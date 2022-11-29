import './Task1.css';
import React, { useState } from "react";

import VideoReader from "../VideoReader/VideoReader";
import QRData from "../QRData/QRData";

import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import Box from '@mui/material/Box';
import TelemetryReceiver from "../TelemetryReceiver/TelemetryReceiver";

function Task1() {

    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        minHeight: '40vh'
      }));

    const [qrReady, setQrReady] = useState("0");
    return (
        <Box sx={{ flexGrow: 1 }} className="Task1">
            <Grid container spacing={2}>
                <Grid xs={6}>
                    <Item>
                        {/* Component QR Reader */}
                        <VideoReader opts={[{value: 1, text: 'One'}, {value: 2, text: 'Two'}]} setQrReady={setQrReady}/>
                    </Item>
                </Grid>
                <Grid xs={6}>
                    <Item><TelemetryReceiver/></Item>
                </Grid>
                <Grid xs={6}>
                    <Item>Component Here</Item>
                </Grid>
                <Grid xs={6}>
                    <Item><QRData qrType="1" qrReady={qrReady === 1}></QRData></Item>
                    <Item><QRData qrType="2" qrReady={qrReady === 2}></QRData></Item>
                </Grid>
            </Grid>
        </Box>
    );
}

export default Task1;
