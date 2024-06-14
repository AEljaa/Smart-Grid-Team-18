import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import './Home.css';
import { Link } from 'react-router-dom';

export default function Home() {
  const [sunIntensity, setSunIntensity] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);
  const [demand, setDemand] = useState(0);
  //const [GeneratedPow,setGen] = useState(0);
  //const [StoredPow,setStor] = useState(0);
  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch("http://127.0.0.1:4000/webdata");
        let data = await response.json();
        setSunIntensity(data.sun);

        setBuyPrice(data.buy_price);
        setSellPrice(data.sell_price);
        setDemand(data.demand);
        
        response = await fetch("http://127.0.0.1:4000/forward_cap_data")
        let gridData = await response.json()
        //setGen(gridData)
        //setStor(gridData)//maybe .stored

      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);
  return (
    <div className="container">
      <NavBar />
      <div className="content">
        <h1 className="title">Current Energy Information</h1>
        <div className="scroll-wrapper">
          <div className="scroll-container">
            <div className="text-box">
              <h2 className="text-label">Sun Irradiance</h2>
              <p className="text-value">{sunIntensity}%</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">Instantaneous Demand </h2>
              <p className="text-value">{demand.toFixed(3)}W</p>
            </div>            
            <div className="text-box">
              <h2 className="text-label">External Sell Price Per Joule</h2>
              <p className="text-value">£{(sellPrice/100).toFixed(2)}</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">External Buy Price Per Joule</h2>
              <p className="text-value">£{(buyPrice/100).toFixed(2)}</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">Generated Solar Power</h2>
              <p className="text-value">Put Generated Pow lifetimeW</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">Stored Power</h2>
              <p className="text-value">capdataW</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
