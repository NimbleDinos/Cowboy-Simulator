using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bob : MonoBehaviour
{
    public GameObject playerPrefab;
    public List< GameObject > Players;
    public void CreatePlayer(Join data)
    {
        GameObject Player = Instantiate(playerPrefab);

        Player.name = data.playerId.ToString();

        Player.GetComponent<PlayerGoToPlaceScript>().name = data.playerName;

        Player.GetComponent<PlayerGoToPlaceScript>().Setup();

        Players.Add(Player);

    }


}
