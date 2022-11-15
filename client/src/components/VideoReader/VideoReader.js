import React, { useState } from 'react'
import { QrReader } from 'react-qr-reader'
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import "./VideoReader.css"

function Camera(props) {
    if(!props.camera) {
        return (
            <div></div>
        )
    }
    return (
        <>
            <QrReader
                onResult={(res, err) => {
                    // !! cast 'res' to type boolean
                    if(!!res) {
                        // ?. returns undef instead of throwing err
                        props.setQrRaw(res ? res.text : null)
                    }
                    if(!!err) {
                        console.info(err)
                    }
                }}
                className="qr-reader"
            />
            <p className='reader-text'>{props.qrRaw}</p>
        </>
    )
}

function VideoReader() {
    const [qrRaw, setQrRaw] = useState("No Result")
    const [camera, setCamera] = useState(false)

    return (
        <>
            <ButtonGroup className='qr-controls' variant='contained' aria-label='outlined primary button group'>
                <Button disabled={camera === true} onClick={() => {setCamera(true)}}>ON</Button>
                <Button disabled={camera === false} onClick={() => {setCamera(false)}}>OFF</Button>
            </ButtonGroup>
            <br/>
            <Camera camera={camera} setQrRaw={setQrRaw} qrRaw={qrRaw}/>
        </>
    )
}

export default VideoReader
