import './Task2.css';
import React from "react";
import VideoReader from "../VideoReader/VideoReader";
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import Box from '@mui/material/Box';

function Task2() {

    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        minHeight: '40vh'
      }));

    return (
        <Box sx={{ flexGrow: 1 }} className="Task2">
            <Grid container spacing={2}>
                <Grid xs={6}>
                    <Item>
                        {/* Component QR Reader */}
                        <VideoReader opts={[{value: 3, text: 'Three'}]}/>
                    </Item>
                </Grid>
                <Grid xs={6}>
                    <Item>Component Here</Item>
                </Grid>
                <Grid xs={6}>
                    <Item>Component Here</Item>
                </Grid>
                <Grid xs={6}>
                    <Item>Component Here</Item>
                </Grid>
            </Grid>
        </Box>
    );
}

export default Task2;