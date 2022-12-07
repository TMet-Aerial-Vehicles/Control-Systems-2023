import React, {useEffect, useState} from "react";
import io from "socket.io-client"

const socket = io('/')

function TelemetryReceiver() {
    const [dataObj, setData] = useState(
        ""
    )
    useEffect(() => {
        socket.on("telemetry", msg => {
            console.log(msg)
            setData(msg)
        })
        // Listener cleanup after setup
        return () => {
            socket.off('telemetry');
          };
    }, []);

    
    return (
        <>
            <h1>Longitude:{dataObj.longitude}</h1>
            <h1>Latitude:{dataObj.latitude}</h1>
            <h1>Height:{dataObj.height}</h1>
            <h1>Time:{dataObj.timestamp}</h1>
        </>
    )
}

export default TelemetryReceiver
