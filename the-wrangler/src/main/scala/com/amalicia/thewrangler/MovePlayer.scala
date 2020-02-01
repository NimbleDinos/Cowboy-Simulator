package com.amalicia.thewrangler

case class MovePlayer(userId: Long, town: Option[String], place: Option[String], time: Int)

object MovePlayer {
  final case class PlayerMovementException(message: String) extends Exception

  val townList  = List("hull", "lincoln", "sheffield")
  val placeList = List("corral", "gold-mine", "plains", "river", "shooting-range")

  def xor[T](x: Option[T], y: Option[T]): (Option[T], Boolean) = (x, y) match {
    case (Some(_), None) ⇒ (x, true)
    case (None, Some(_)) ⇒ (y, false)
    case _               ⇒ (None, false)
  }

  def validatePlayerMovement(userId: Long, town: Option[String], place: Option[String], time: Int): Either[PlayerMovementException, MovePlayer] = {
    val (maybeTownPlace, isTown) = xor(town, place)
    maybeTownPlace.toRight(PlayerMovementException("Only a single town or place can be present")).flatMap { townPlace ⇒
      if (isTown) validateTown(townPlace.toLowerCase()).map(town ⇒ MovePlayer(userId, Some(town), None, time))
      else validatePlace(townPlace.toLowerCase()).map(place ⇒ MovePlayer(userId, None, Some(place), time))
    }
  }

  def validateTown(town: String): Either[PlayerMovementException, String] =
    if (townList.contains(town)) Right(town) else Left(PlayerMovementException(s"$town is not a valid town"))

  def validatePlace(place: String): Either[PlayerMovementException, String] =
    if (placeList.contains(place)) Right(place) else Left(PlayerMovementException(s"$place is not a valid place"))
}
