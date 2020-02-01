package com.amalicia.thewrangler

case class MovePlayer(userId: Long, place: String, time: Int)

object MovePlayer {
  final case class PlayerMovementException(message: String) extends Exception

  val placeList = List("corral", "gold-mine", "plains", "river", "shooting-range", "hull", "lincoln", "sheffield")

  def validatePlayerMovement(userId: Long, place: String, time: Int): Either[PlayerMovementException, MovePlayer] =
    if (placeList.contains(place)) {
      Right(MovePlayer(userId, place, time))
    } else {
      Left(PlayerMovementException(s"$place is not a valid location"))
    }
}
