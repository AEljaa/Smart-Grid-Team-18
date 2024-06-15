import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import './Home.css';
import { Link } from 'react-router-dom';

export default function Home() {
  const [sunIntensity, setSunIntensity] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);
  const [currBuy,setCurrBuy] = useState(0);
  const [currSell,setCurrSell] = useState(0);
  const [demand, setDemand] = useState(0);
  //const [GeneratedPow,setGen] = useState(0);
  //const [StoredPow,setStor] = useState(0);

  let startTime, endTime, duration;
  useEffect(() => {
    const fetchData = async () => {
      try {
        startTime = performance.now();
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

        endTime = performance.now();
        duration = endTime - startTime;
        console.log(duration)
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);
//Grid values change more frequently so needs own fetching
useEffect(() => {
    const fetchGridData = async () => {
      try {
        let response = await fetch("http://127.0.0.1:4000/forward_grid_data")
        let gridData = await response.json()
        setCurrBuy(gridData.buy)//how much we just bought
        setCurrSell(gridData.sell) //how much we just sold
      } catch (error) {
        console.error(error);
      }
    };

    fetchGridData();
    const interval = setInterval(fetchGridData, 100);//grid changes every 100ms
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
              <p className="text-value">{0}J</p>
          </div>
          <div className="text-box">
              <h2 className="text-label">Exported Energy Amount</h2>
              <p className="text-value">{3}J</p>
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
              <p className="text-value">27J</p>
        </div>
        </div>
    </div>
    </div>
  );
}
