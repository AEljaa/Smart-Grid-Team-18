import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import { Link } from 'react-router-dom';
import './Energy.css';

export default function Home() {
  const [currBuy,setCurrBuy] = useState(0);
  const [currSell,setCurrSell] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        response = await fetch("http://127.0.0.1:4000/forward_grid_data")
        let gridData = await response.json()
        setCurrBuy(currBuy.buy)//how much we just bought
        setCurrSell(currSell.sell) //how much we just sold
        
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
            <div className="text-box">
              <h2 className="text-label">Exported Energy Value</h2>
              <p className="text-value">£{(currBuy*sellPrice)/100}</p>
            </div>
           <div className="text-box">
              <h2 className="text-label">Imported Energy Value</h2>
              <p className="text-value">£{(currSell*buyPrice)/100}</p>
           </div>
      </div>
    </div>
  );
}

