package com.amalicia.thewrangler

import cats.effect.IO
import com.twitter.finagle.{ Http, Service }
import com.twitter.finagle.http.{ Request, Response }
import com.twitter.util.Await
import io.circe.Json
import io.finch._
import io.finch.catsEffect._
import io.finch.circe._
import io.circe.generic.auto._
import io.circe.syntax._

import scala.collection.mutable.ListBuffer

object Main extends App {

  case class Message(hello: String)

  val joinQueue = scala.collection.mutable.Queue[JoinGame]()

  val playerMoveList = new ListBuffer[MovePlayer]()

  def healthcheck: Endpoint[IO, String] = get(pathEmpty) {
    Ok("OK")
  }

  def join: Endpoint[IO, String] = get("join" :: param[Long]("userId") :: param[String]("userName")) { (userId: Long, userName: String) ⇒
    joinQueue.enqueue(JoinGame(userId, userName))
    Ok(s"Player ID: $userId added to Join Queue")
  }

  def getJoin: Endpoint[IO, Json] = get("getJoin") {
    if (joinQueue.isEmpty) Ok(JoinGame(-1, "").asJson)
    else Ok(joinQueue.dequeue().asJson)
  }

  def movePlayer: Endpoint[IO, String] =
    get("movePlayer" :: param[Long]("userId") :: paramOption[String]("town") :: paramOption[String]("place") :: param[Int]("time")) {
      (userId: Long, town: Option[String], place: Option[String], time: Int) ⇒
        val validPlayerMovement = MovePlayer.validatePlayerMovement(userId, town, place, time)
        validPlayerMovement.fold(error ⇒ BadRequest(error), move ⇒ { playerMoveList += move; Ok(s"Move update for userId=$userId added to list") })
    }

  def getMovements: Endpoint[IO, Json] = get("getMovement") {
    val moveList = playerMoveList.toList
    playerMoveList --= moveList
    Ok(moveList.asJson)
  }

  def service: Service[Request, Response] =
    Bootstrap
      .serve[Text.Plain](healthcheck :+: join :+: movePlayer)
      .serve[Application.Json](getJoin :+: getMovements)
      .toService

  Await.ready(Http.server.serve(":8081", service))
}
