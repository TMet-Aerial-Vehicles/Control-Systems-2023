import React, {useState} from "react";
import {wait} from "@testing-library/user-event/dist/utils";

function TelemetryReceiver() {
    const [dataObj, setData] = useState(
        {
            longitude: "Longitude",
            latitude: "Latitude",
            height: "Height",
            time: "Time"
        }
    )

    fetch("http://127.0.0.1:5000/recent-telemetry")
        .then(response => response.json())
        .then(data => {

            setData({
                ...dataObj,
                longitude: data.data.longitude,
                latitude: data.data.latitude,
                height: data.data.height,
                time: data.data.time
            })

        })
    return (
        <>
            <h1>Longitude:{dataObj.longitude}</h1>
            <h1>Latitude:{dataObj.latitude}</h1>
            <h1>Height:{dataObj.height}</h1>
            <h1>Time:{dataObj.time}</h1>
        </>
    )
}

export default TelemetryReceiver
