import axios from 'axios';
import React, { useState, useEffect } from 'react';

function QRData(props) {

    const [qrData, setQrData] = useState({"success": false, "qr_type": "", "qr_data": {"is_found": false}});
    // console.log(props.qrReady)
    useEffect(() => {
        console.log("Affected")
        console.log(props.qrReady)
        axios.get(`/get_parsed_qr/${props.qrType}`)
        .then((response) => {
            console.log(response.data);
            setQrData(response.data)
        })
        .catch(error => console.error(`Error: ${error}`));
    }, [props.qrReady])
    

    // const getQrData = () => {
    //     axios.get(`/get_parsed_qr/${props.qr_type}`)
    //         .then((response) => {
    //             const returnedData = response.data;
    //             console.log(returnedData);
    //         })
    //         .catch(error => console.error(`Error: ${error}`));
    // }
    // {
    //     success
    //     qr_type
    //     qr_data : {
    //         routes 
    //         is_found
    //         raw_qr_string
    //     }
    // }

    if (qrData.qr_data.is_found === false) {
        return <><h1>QR {props.qrType} Not Ready</h1></>
    }
    else if (props.qrType === "1") {
        return (
            <>
                <h1>{qrData.success}</h1>
                <h1>{qrData.qr_type}</h1>
    
                <h1>Routes</h1>
    
                {qrData.qr_data.routes !== undefined ? qrData.qr_data.routes.map((waypoint) => {
                    console.log("FOUND")
                    return (
                        <>
                        <h3>Waypoint {waypoint.name} #{waypoint.number}</h3>
                        <h4>Longitude: {waypoint.longitude}</h4>
                        <h4>Latitude: {waypoint.latitude}</h4>
                        </>
                    )
                }) : null}
            </>
        )
    } else if (props.qrType === "2") {
        return <><h1>Q2</h1></>
    } else {
        return <><h1>Unknown QR Type</h1></>
    }

    
}

export default QRData