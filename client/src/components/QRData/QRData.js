import axios from 'axios';
import React, { useState, useEffect } from 'react';

function QRData(props) {

    const [qrData, setQrData] = useState({"success": false, "qr_type": "", "qr_data": {"is_found": false}});

    useEffect(() => {
        console.log(props.qrReady)
        axios.get(`/get_parsed_qr/${props.qrType}`)
        .then((response) => {
            console.log(response.data);
            setQrData(response.data)
        })
        .catch(error => console.error(`Error: ${error}`));
    }, [props.qrReady]);

    if (qrData.qr_data.is_found === false) {
        return <><h1>QR {props.qrType} Not Ready</h1></>
    } else if (props.qrType === "1") {
        return <QR1Data qrData={qrData}/>
    } else if (props.qrType === "2") {
        return <QR2Data qrData={qrData}/>
    } else if (props.qrType === "3") {
        return <QR3Data qrData={qrData}/>
    } else {
        return <><h1>Unknown QR Type</h1></>
    }

}

function Waypoint(waypoint) {
    return <>
        <h4>Waypoint {waypoint.waypoint.name} #{waypoint.waypoint.number}</h4>
        <h5>Longitude: {waypoint.waypoint.longitude}, Latitude: {waypoint.waypoint.latitude}</h5>
    </>
}

function QR1Data({qrData}) {
    return <>
        <h1>QR {qrData.qr_type}</h1>

        <h2>Routes</h2>
        {qrData.qr_data.routes !== undefined ?
            qrData.qr_data.routes.map((waypoint) => {
                return <Waypoint key={waypoint.number} waypoint={waypoint}/>
            }) : null
        }
    </>
}

function QR2Data({qrData}) {
    return <>
        <h1>QR {qrData.qr_type}</h1>

        <h2>Boundaries</h2>
        {qrData.qr_data.boundaries !== undefined ?
            qrData.qr_data.boundaries.map((waypoint) => {
                return <Waypoint key={waypoint.number} waypoint={waypoint}/>
            }) : null
        }
        <br/>
        <h2>Rejoin at Waypoint:</h2>
        {qrData.qr_data.rejoin_waypoint !== undefined ? (
            <Waypoint key={qrData.qr_data.rejoin_waypoint.number} waypoint={qrData.qr_data.rejoin_waypoint}/>
        ) : null}
    </>
}

function QR3Data({qrData}) {
    return <>
        <h1>QR {qrData.qr_type}</h1>

        <h2>Routes</h2>
        {qrData.qr_data.routes !== undefined ?
            qrData.qr_data.routes.map((waypoint) => {
                return <Waypoint key={waypoint.number} waypoint={waypoint}/>
            }) : null
        }
    </>
}

export default QRData
