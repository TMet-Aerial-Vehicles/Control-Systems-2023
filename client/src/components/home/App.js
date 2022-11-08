import './App.css';
import {useEffect, useState} from "react";
import axios from "axios";
import QrReader from "../QrReader/QrReader";

function App() {
    const [test, setTest] = useState("");
    useEffect(() => {
        axios.get("/testing").then(res => {
            console.log("SUCCESS", res);
            setTest(res.data);
        }).catch(error => {
            console.log(error)
        })
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <p>
                    {test.body}
                </p>
            </header>
            <QrReader></QrReader>
        </div>
    );
}

export default App;
