package com.amalicia.thewrangler

import cats.effect.IO
import com.twitter.finagle.{Http, Service}
import com.twitter.finagle.http.{Request, Response}
import com.twitter.util.Await
import io.circe.Json
import io.finch._
import io.finch.catsEffect._
import io.finch.circe._
import io.circe.generic.auto._
import io.circe.syntax._

object Main extends App {

  case class Message(hello: String)

  val joinQueue = scala.collection.mutable.Queue[Long]()

  def healthcheck: Endpoint[IO, String] = get(pathEmpty) {
    Ok("OK")
  }

  def join: Endpoint[IO, String] = get("join" :: param[Long]("userId")) {
    (userId: Long) ⇒
      joinQueue.enqueue(userId)
      Ok(s"Player ID: $userId added to Join Queue" )
  }

  def getJoin: Endpoint[IO, Json] = get("getJoin") {
    if (joinQueue.isEmpty) Ok((-1).asJson)
    else Ok(joinQueue.dequeue().asJson)
  }

  def service: Service[Request, Response] = Bootstrap
    .serve[Text.Plain](healthcheck)
    .serve[Application.Json](join :+: getJoin)
    .toService

  Await.ready(Http.server.serve(":8081", service))
}