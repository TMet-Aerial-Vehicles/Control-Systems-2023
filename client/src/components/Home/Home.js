import './Home.css';
import React, {useEffect, useState} from "react";
import axios from "axios";
import VideoReader from "../VideoReader/VideoReader";
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import Box from '@mui/material/Box';

function Home() {
    const [test, setTest] = useState("");
    useEffect(() => {
        axios.get("/testing").then(res => {
            console.log("SUCCESS", res);
            setTest(res.data.body);
        }).catch(error => {
            console.log(error)
        })
    }, []);

    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        minHeight: '40vh'
      }));

    return (
        <Box sx={{ flexGrow: 1 }} className="Home">
            <Grid container spacing={2}>
                <Grid xs={6}>
                    <Item>
                        {/* Component QR Reader */}
                        <VideoReader/>
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

export default Home;
