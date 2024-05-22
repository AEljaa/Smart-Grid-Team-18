import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import { Link } from 'react-router-dom';
import './Energy.css';

export default function Energy() {
//   const [data, setData] = useState({});

//   const fetchData = async () => {
//     try {
//       const response = await fetch('https://your-webserver-endpoint.com/data'); // Get the data from the server
//       const result = await response.json();
//       setData(result);
//     } catch (error) {
//       console.error(error);
//     }
//   };

//   useEffect(() => {
//     fetchData();
//     const interval = setInterval(fetchData, 5000);
//     return () => clearInterval(interval);
//   }, []);

  return (
    <div className="container">
      <NavBar />
      <h1 className="title">Energy Trading</h1>
      <div className="textBox">
        <h2 className="textLabel">Import Cost</h2>
        <p className="textValue">{2}</p>
        <button className="button" onClick={() => console.log("Import")}>
          Import
        </button>
      </div>
      <div className="textBox">
        <h2 className="textLabel">Export Cost</h2>
        <p className="textValue">{3}</p>
        <button className="button" onClick={() => console.log("Export")}>
          Export
        </button>
      </div>
      <Link to="/" className="link">Go to Home</Link>
    </div>
  );
}
