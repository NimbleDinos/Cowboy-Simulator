using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class PlayerGoToPlaceScript : MonoBehaviour
{
    public GameObject objHull, objMine, objShefuel, objGrimstone, objhorseRide, objHorseCatch;
    Transform Target; 

    GameObject[] Places;

    // Start is called before the first frame update
    public void Setup()
    {
        Places = GameObject.FindGameObjectsWithTag("Place");

        for (int i = 0; i < Places.Length; i++)
        {
            switch(Places[i].name)
            {
                case "Hull":
                    objHull = Places[i];
                    break;
                case "Shefuel":
                    objShefuel = Places[i];
                    break;
                case "Grimstone":
                    objGrimstone = Places[i];
                    break;
                case "HorseRide":
                    objhorseRide= Places[i];
                    break;
                case "HorseCatch":
                    objHorseCatch = Places[i];
                    break;
                case "Mine":
                    objMine = Places[i];
                    break;
            }
        }

    }

    private void Update()
    {

        transform.position = Vector3.MoveTowards(transform.position, Target.position, (2 * Time.deltaTime));

    }



    public void Hull()
    {
        Target = objHull.transform;
    }

    public void SheFuel()
    {
        Target = objShefuel.transform;
    }

    public void GrimStone()
    {
        Target = objGrimstone.transform;
    }

    public void HorseRide()
    {
        Target = objhorseRide.transform;
    }

    public void HorseCatch()
    {
        Target = objHorseCatch.transform;
    }
    public void Mine()
    {
        Target = objMine.transform;
    }


}

[CustomEditor(typeof(PlayerGoToPlaceScript))]
public class CityGenButts : Editor
{
    public override void OnInspectorGUI()
    {
        base.OnInspectorGUI();
        {

            PlayerGoToPlaceScript script = (PlayerGoToPlaceScript)target;

            if(GUILayout.Button("Setup"))
            {
                script.Setup();
            }

            if (GUILayout.Button("GoTo Shefuel"))
            {
                script.SheFuel();
            }

            if (GUILayout.Button("GoTo GrimStone"))
            {
                script.GrimStone();
            }

            if (GUILayout.Button("GoTo Hull"))
            {
                script.Hull();
            }

            if (GUILayout.Button("GoTo Catch Horse"))
            {
                script.HorseCatch();
            }

            if (GUILayout.Button("GoTo Ride Horse"))
            {
                script.HorseRide();
            }

            if (GUILayout.Button("GoTo Mine For Gold"))
            {
                script.Mine();
            }
        }
    }
}
