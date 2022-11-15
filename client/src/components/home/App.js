import './App.css';
import React, {useEffect, useState} from "react";
import axios from "axios";
import VideoReader from "../VideoReader/VideoReader";

function App() {
    const [test, setTest] = useState("");
    useEffect(() => {
        axios.get("/testing").then(res => {
            console.log("SUCCESS", res);
            setTest(res.data.body);
        }).catch(error => {
            console.log(error)
        })
    }, []);

    return (
        <div className="App">
            <header className='app-header'>
                // TMAV
            </header>
            <br/>
            <p>
               Test Data: {test}
            </p>
            <br/>
            <VideoReader/>
        </div>
    );
}

export default App;
