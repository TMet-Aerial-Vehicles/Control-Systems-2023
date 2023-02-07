import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import './index.css';

import Layout from './components/Layout/Layout';
import Home from './components/Home/Home';
import Task1 from './components/Task1/Task1';
import Task2 from './components/Task2/Task2';


export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                    <Route path="task-1" element={<Task1 />} />
                    <Route path="task-2" element={<Task2 />} />
                    <Route path="*" element={<Home />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
