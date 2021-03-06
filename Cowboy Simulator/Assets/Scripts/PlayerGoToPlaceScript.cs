﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class PlayerGoToPlaceScript : MonoBehaviour
{
    public GameObject objHull, objMine, objSheffield, objLincoln, objhorseRide, objHorseCatch, objShot, objRiver;
    Transform TargObj;
    Vector3 Target;
    public string name;

    public float tim = 10, timer = 0;

    GameObject[] Places;


    // Start is called before the first frame update
    public void Setup()
    {
        Places = GameObject.FindGameObjectsWithTag("Place");

        this.transform.GetComponentInChildren<TextMesh>().text = name;
        this.transform.GetComponentInChildren<MeshRenderer>().sortingLayerName = "Top";

        for (int i = 0; i < Places.Length; i++)
        {
            switch(Places[i].name)
            {
                case "Hull":
                    objHull = Places[i];
                    break;
                case "Sheffield":
                    objSheffield = Places[i];
                    break;
                case "Lincoln":
                    objLincoln = Places[i];
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
                case "Shot":
                    objShot = Places[i];
                    break;
                case "River":
                    objRiver = Places[i];
                    break;
            }
        }

        Hull();


        this.GetComponent<SpriteRenderer>().color = new Color32((byte)Random.Range(0, 256), (byte)Random.Range(0, 256), (byte)Random.Range(0, 256),  255);

    }

    void RandPos()
    {
        timer = 0;
        tim = Random.Range(5, 11);

        Target = TargObj.position + new Vector3(Random.Range(0, 3) - 1, Random.Range(0, 3) - 1, 0);
    }

    private void Update()
    {
        timer += Time.deltaTime;

        if (timer > tim)
            RandPos();
            

        Vector3 Direction = Vector3.MoveTowards(transform.position, Target, (2 * Time.deltaTime));

        if (Direction.x > transform.position.x && transform.GetComponent<Animator>().GetBool("isWalk"))
        {
            this.transform.localScale = new Vector3(-.1f, .1f, .1f);
            this.transform.GetComponentInChildren<TextMesh>().transform.localScale = new Vector3(-.3f, .3f, .3f);
        }
        else if (transform.GetComponent<Animator>().GetBool("isWalk"))
        {
            this.transform.localScale = new Vector3(.1f, .1f, .1f);
            this.transform.GetComponentInChildren<TextMesh>().transform.localScale = new Vector3(.3f, .3f, .3f);
        }
        transform.position = Direction;

        if(Vector3.Distance(transform.position, Target) > .1)
        {
            this.GetComponent<Animator>().SetBool("isWalk", true);
        }
        else
            this.GetComponent<Animator>().SetBool("isWalk", false);


    }



    public void Hull()
    {
        TargObj = objHull.transform;
        Target = TargObj.position;
    }

    public void Sheffield()
    {
        TargObj= objSheffield.transform;
        Target = TargObj.position;
    }

    public void Lincoln()
    {
        TargObj= objLincoln.transform;
        Target = TargObj.position;
    }
    public void HorseRide()
    {
        TargObj= objhorseRide.transform;
        Target = TargObj.position;
    }

    public void HorseCatch()
    {
        TargObj= objHorseCatch.transform;
        Target = TargObj.position;
    }

    public void Mine()
    {
        TargObj = objMine.transform;
        Target = TargObj.position;
    }
    public void Shot()
    {
        TargObj = objShot.transform;
        Target = TargObj.position;
    }

    public void River()
    {
        TargObj = objRiver.transform;
        Target = TargObj.position;
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

            if (GUILayout.Button("GoTo Sheffield"))
            {
                script.Sheffield();
            }

            if (GUILayout.Button("GoTo Lincoln"))
            {
                script.Lincoln();
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

            if (GUILayout.Button("GoTo Shoot"))
            {
                script.Shot();
            }

            if(GUILayout.Button("GoTo River"))
            {
                script.River();
            }
        }
    }
}
