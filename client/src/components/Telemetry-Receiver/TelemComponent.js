import React, {useState} from "react";

function TelemComponent(){
    const [dataObj,setData] = useState (
        {
            longtitude: "longtitude",
            lat: "lat",
            height: "height",
            time: "time"
        }
    )
    

      fetch("http://127.0.0.1:5000/recent-telemetry")
      .then(response => response.json())
      .then(data => {

        console.log(data.data)
        setData({
            ...dataObj,
            longtitude : data.data.longtitude,
            lat : data.data.lat,
            height : data.data.height,
            time : data.data.time
        })
       
      })
    return(
    <>
    <h1>Longtitude:{dataObj.longtitude}</h1>
    <h1>Latitude:{dataObj.lat}</h1>
    <h1>Height:{dataObj.height}</h1>
    <h1>Time:{dataObj.time}</h1>
    </>
    )  
}
export default TelemComponent
