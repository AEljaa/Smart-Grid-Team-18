import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import { Link } from 'react-router-dom';
import './Energy.css';

export default function Energy() {
  const [currBuy,setCurrBuy] = useState(0);
  const [currSell,setCurrSell] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        response = await fetch("http://127.0.0.1:4000/forward_grid_data")
        let gridData = await response.json()
        setCurrBuy(gridData.imp)//how much we just bought
        setCurrSell(gridData.exp) //how much we just sold
        
        let response = await fetch("http://127.0.0.1:4000/webdata");
        let data = await response.json();
        setBuyPrice(data.buy_price);
        setSellPrice(data.sell_price);

      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 100);//grid changes every 100ms
    return () => clearInterval(interval);
  }, []);
  return (
    <div className="container">
      <NavBar />
      <div className="content">
        <h1 className="title">Current Grid Information</h1>
      <div className="text-boxes">
          <div className="text-boxe">
            <h2 className="text-label">Exported Energy Value</h2>
            <p className="text-value">£{(currSell * sellPrice) / 100}</p>
          </div>
          <div className="text-boxe">
            <h2 className="text-label">Imported Energy Value</h2>
            <p className="text-value">£{(currBuy * buyPrice) / 100}</p>
          </div>
          <div className="text-boxe">
            <h2 className="text-label">Profit</h2>
            <p className="text-value">£{((currSell * sellPrice) - (currBuy * buyPrice)) / 100}</p>
          </div>
      </div>
    </div>
    </div>
  );
}

