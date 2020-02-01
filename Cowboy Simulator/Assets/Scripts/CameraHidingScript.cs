using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraHidingScript : MonoBehaviour
{
    public bool PlayerOr = false;

    // Start is called before the first frame update
    void Update()
    {
        if(PlayerOr)
            GetComponent<Camera>().cullingMask = (1 << 1);
        else
            GetComponent<Camera>().cullingMask = (1 << 0);

    }

}
