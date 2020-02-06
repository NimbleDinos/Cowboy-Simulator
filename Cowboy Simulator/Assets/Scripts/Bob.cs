using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bob : MonoBehaviour
{
    public GameObject playerPrefab;
    public List< GameObject > Players;
    public float time = 0, callInterval = 0;

    private void Update()
    {
        time += Time.deltaTime;

        if (time >= callInterval)
        {
            time = 0;

            this.GetComponent<WranglerHelper>().enabled = true;
            Debug.Log("Call Update");
        }

    }


    public void MovePlayer(Movement data)
    {
        foreach (var item in Players)
        {
            if(item.name == data.userId.ToString())
            {
                switch(data.place)
                {
                    case "hull":
                        item.GetComponent<PlayerGoToPlaceScript>().Hull();
                        break;
                    case "sheffield":
                        item.GetComponent<PlayerGoToPlaceScript>().Sheffield();
                        break;
                    case "lincoln":
                        item.GetComponent<PlayerGoToPlaceScript>().Lincoln();
                        break;
                    case "corral":
                        item.GetComponent<PlayerGoToPlaceScript>().HorseRide();
                        break;
                    case "gold-mine":
                        item.GetComponent<PlayerGoToPlaceScript>().Mine();
                        break;
                    case "plains":
                        item.GetComponent<PlayerGoToPlaceScript>().HorseCatch();
                        break;
                    case "shooting-range":
                        item.GetComponent<PlayerGoToPlaceScript>().Shot();
                        break;
                    case "river":
                        item.GetComponent<PlayerGoToPlaceScript>().River();
                        break;
                }
            }
        }
    }

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
