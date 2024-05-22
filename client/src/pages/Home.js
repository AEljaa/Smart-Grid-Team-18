import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar'; // Make sure this component is also converted
import './Home.css'; // Import the CSS file for styling
import ReactDOM from 'react-dom/client';
import './Home.css';
import reportWebVitals from '../reportWebVitals';
import { Link } from 'react-router-dom';
export default function Home() {
  // Assuming you have the data fetching logic here
  // const [data, setData] = useState({});
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch('https://your-webserver-endpoint.com/data');
  //       const result = await response.json();
  //       setData(result);
  //     } catch (error) {
  //       console.error(error);
  //     }
  //   };
  //   fetchData();
  //   const interval = setInterval(fetchData, 5000);
  //   return () => clearInterval(interval);
  // }, []);

  return (
    <div className="container">
      <NavBar />
      <div className="content">
        <h1 className="title">Current Energy Information</h1>
        <div className="scroll-wrapper">
        <div className="scroll-container">
          <div className="text-box">
            <h2 className="text-label">Sun Irradiance</h2>
            <p className="text-value">{73}W/m2</p>
          </div>
          <div className="text-box">
            <h2 className="text-label">Instantaneous Demand</h2>
            <p className="text-value">{45}W</p>
          </div>
          <div className="text-box">
            <h2 className="text-label">Price Per Watt</h2>
            <p className="text-value">£{0.37}</p>
          </div>
          <div className="text-box">
            <h2 className="text-label">Generated Solar Power</h2>
            <p className="text-value">{100}W</p>
          </div>
          <div className="text-box">
            <h2 className="text-label">Stored Power</h2>
            <p className="text-value">{23}W</p>
          </div>
        </div>
        </div>
        <Link to="/energy" className="link">Go to Energy Trading</Link>
      </div>
    </div>
  );
}
