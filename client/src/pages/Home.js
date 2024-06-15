
import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import './Home.css';
import { Link } from 'react-router-dom';

export default function Home() {
  const [sunIntensity, setSunIntensity] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);
  const [currImp, setCurrImp] = useState(0);
  const [currExp, setCurrExp] = useState(0);
  const [demand, setDemand] = useState(0);
  const [storedEnergy, setStoredEnergy] = useState(0); 

  useEffect(() => {
    const fetchData = async () => {
      try {
        let startTime = performance.now();

        let response = await fetch("http://127.0.0.1:4000/webdata")
        let webData= await response.json()

        setSunIntensity(webData.sun);
        setBuyPrice(webData.buy_price);
        setSellPrice(webData.sell_price);
        setDemand(webData.demand);

        response = await fetch("http://127.0.0.1:4000/forward_cap_data")
        let capData= await response.json()
        console.log(capData)

        setStoredEnergy(capData.message != "No data available" ? capData : 0); 

        response = await fetch("http://127.0.0.1:4000/forward_grid_data")
        let gridData = await response.json()
       
        setCurrImp(gridData.value > 0 ? gridData.value : 0);// if value form grid is positive then imported
        setCurrExp(gridData.value < 0 ? gridData.value : 0); // if negative then we exported
        console.log(gridData)

        let endTime = performance.now();
        console.log(`Duration: ${endTime - startTime}ms`);
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
              <h2 className="text-label">Imported Energy Amount</h2>
              <p className="text-value">{currImp}J</p>
          </div>
          <div className="text-box">
              <h2 className="text-label">Exported Energy Amount</h2>
              <p className="text-value">{currExp}J</p>
          </div>
            <div className="text-box">
              <h2 className="text-label">External Sell Price Per Joule</h2>
              <p className="text-value">£{(sellPrice/100).toFixed(2)}</p>
            </div>
            <div className="text-box">
              <h2 className="text-label">External Buy Price Per Joule</h2>
              <p className="text-value">£{(buyPrice/100).toFixed(2)}</p>
            </div>
        </div>
            <div className="text-box">
              <h2 className="text-label">Current Stored Energy</h2>
              <p className="text-value">{storedEnergy}J</p>
        </div>
        </div>
    </div>
    </div>
  );
}
