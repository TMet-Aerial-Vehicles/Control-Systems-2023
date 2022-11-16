import './Home.css';
import React, {useEffect, useState} from "react";
import axios from "axios";

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

    return (
        <div className="Home">
            <header className='app-header'>
                TMAV
            </header>
            <br/>
            <p>
               Test Data: {test}
            </p>
        </div>
    );
}

export default Home;