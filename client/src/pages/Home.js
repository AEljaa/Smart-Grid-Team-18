import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import './Home.css';
import { Link } from 'react-router-dom';

export default function Home() {
  const [sunIntensity, setSunIntensity] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);
  const [demand, setDemand] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch("http://localhost:4000/sun");
        let sunData = await response.json();
        setSunIntensity(sunData.sun);

        response = await fetch("http://localhost:4000/price");
        let priceData = await response.json();
        setBuyPrice(priceData.buy_price);
        setSellPrice(priceData.sell_price);

        response = await fetch("http://localhost:4000/demand");
        let demandData = await response.json();
        setDemand(demandData.demand);
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
              <p className="text-value">{sunIntensity}W/m²</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">Instantaneous Demand</h2>
              <p className="text-value">{Math.round(demand * 1000) / 1000}W</p>
            </div>            
            <div className="text-box">
              <h2 className="text-label">External Sell Price Per Watt</h2>
              <p className="text-value">£{sellPrice}</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">External Buy Price Per Watt</h2>
              <p className="text-value">£{buyPrice}</p>
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
