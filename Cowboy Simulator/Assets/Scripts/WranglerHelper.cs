using System;
using System.Linq;
using System.Threading.Tasks;
using UnityEngine;
using Newtonsoft.Json;

public class WranglerHelper : MonoBehaviour
{

    // Update is called once per frame
    async void Update()
    {
        var join = await GetJoin();

        GetComponent<Bob>().CreatePlayer(join);

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
        Debug.Log(join.playerId);

        return join;
    }
}
