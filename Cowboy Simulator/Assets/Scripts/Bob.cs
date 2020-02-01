using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bob : MonoBehaviour
{
    public GameObject playerPrefab;
    public List< GameObject > Players;
    public void CreatePlayer(Join data)
    {
        bool doExist = false;
        foreach (GameObject check in Players)
        {
            if (check.name == data.playerId.ToString())
            {
                doExist = true;
                break;
            }
        }

        if (!doExist)
        {
            GameObject Player = Instantiate(playerPrefab);

            Player.name = data.playerId.ToString();

            Player.GetComponent<PlayerGoToPlaceScript>().name = data.playerName;

            Player.GetComponent<PlayerGoToPlaceScript>().Setup();

            Players.Add(Player);
        }
        else
        {
            for (int i = 0; i < Players.Count; i++)
            {
                if (Players[i].name == data.playerId.ToString())
                {
                    GameObject temp = Players[i];
                    Players.Remove(temp);
                    DestroyImmediate(temp);
                    break;
                }
            }
        }
    }

}
