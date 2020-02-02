using System;
using System.Linq;
using System.Collections;
using System.Threading.Tasks;
using UnityEngine;
using Newtonsoft.Json;

public class WranglerHelper : MonoBehaviour
{

    // Update is called once per frame
    async void Update()
    {
        var join = await GetJoin();

        if (join.playerId != -1)
        {
            Debug.Log(join.playerId);
            GetComponent<Bob>().CreatePlayer(join);
        }

        var moveList = await GetMovement();

        if (moveList.Count() > 0)
        {
            foreach (var item in moveList)
            {
                GetComponent<Bob>().MovePlayer(item);
            }
        }

    }

    async Task<Join> GetJoin()
    {
        var response = await new WWW("http://localhost:8081/getJoin");
        if (!string.IsNullOrEmpty(response.error))
        {
            throw new Exception();
        }
        var json = response.text;
        var join = JsonConvert.DeserializeObject<Join>(json);
        //Debug.Log(join.playerId);

        return join;
    }

    async Task<Movement[]> GetMovement()
    {
        var response = await new WWW("http://localhost:8081/getMovement");
        if (!string.IsNullOrEmpty(response.error))
        {
            throw new Exception();
        }
        var json = response.text;
        var moveList = JsonConvert.DeserializeObject<Movement[]>(json);

        if (moveList.Any())
        {
            Debug.Log(moveList[0].place);
        }

        return moveList;
    }
}
