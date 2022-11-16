import React, { useState } from 'react'
import { QrReader } from 'react-qr-reader'
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import Grid from '@mui/material/Unstable_Grid2';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

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
        </>
    )
}

function SubmitQR() {
    const [qrType, setQrType] = useState("")
    const handleChange = (event) => {
        setQrType(event.target.value)
    }

    return (
        <Box>
            <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel>QR Type</InputLabel>
                    <Select
                        value={qrType}
                        label="QR Type"
                        autoWidth
                        onChange={handleChange}
                    >
                        <MenuItem value={1}>One</MenuItem>
                        <MenuItem value={2}>Two</MenuItem>
                        <MenuItem value={3}>Three</MenuItem>
                    </Select>
            </FormControl>
            <Button sx={{marginTop: '3%'}} variant='contained'>Submit</Button>
        </Box>
    )
}

function VideoReader() {
    const [qrRaw, setQrRaw] = useState("No Result")
    const [camera, setCamera] = useState(false)

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Grid container spacing={2}>
            <Grid xs={6}>
                    <h3>QR Reader</h3>
                </Grid>
                <Grid xs={6}>
                    <ButtonGroup className='qr-controls' variant='contained' aria-label='outlined primary button group'>
                     <Button disabled={camera === true} onClick={() => {setCamera(true)}}>ON</Button>
                     <Button disabled={camera === false} onClick={() => {setCamera(false)}}>OFF</Button>
                    </ButtonGroup>
                </Grid>
                <Grid xs={6}>
                    <Camera camera={camera} setQrRaw={setQrRaw}/>
                </Grid>
                <Grid xs={6}>
                    <p className='reader-text'>{qrRaw}</p>
                    <SubmitQR/>
                </Grid>
            </Grid>
        </Box>
    )
}

export default VideoReader
