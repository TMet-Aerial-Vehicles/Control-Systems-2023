import axios from "axios";
import React, {useEffect, useState} from "react";
import io from "socket.io-client"

const socket = io('/')

function TelemetryReceiver() {
    const [dataObj, setData] = useState(
        ""
    )
    // Setup Event Subscription
    useEffect(() => {
        socket.on("telemetry", msg => {
            setData(msg)
        })
        // Listener cleanup after setup
        return () => {
            socket.off('telemetry');
          };
    }, []);
    // Pull Latest Telemetry on Re-Render
    useEffect(() => {
        axios.get('/get-telemetry')
            .then((res) => {
                setData(res.data)
            })
    }, [])
    
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
