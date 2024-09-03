import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import { Link } from 'react-router-dom';
import './Energy.css';

export default function Energy() {
  const [currImp,setCurrImp] = useState(0);
  const [currExp,setCurrExp] = useState(0);
  const [buyPrice, setBuyPrice] = useState(0);
  const [sellPrice, setSellPrice] = useState(0);
  const [profit,setProfit] = useState(0);
  useEffect(() => {
    const fetchData = async () => {
      try {

        let startTime = performance.now();
        let response = await fetch("http://127.0.0.1:4000/forward_grid_data")
        let gridData = await response.json()
         
        setCurrImp(Math.abs(gridData.value > 0 ? gridData.value : 0));// if value form grid is positive then imported
        setCurrExp(Math.abs(gridData.value < 0 ? gridData.value : 0)); // if negative then we exported
        setProfit(gridData.profit);

        response = await fetch("http://127.0.0.1:4000/webdata");
        let data = await response.json();
        setBuyPrice(data.buy_price);
        setSellPrice(data.sell_price);


        let endTime = performance.now();
        console.log(`Duration: ${endTime - startTime}ms`);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);//grid changes every 100ms
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
            <p className="text-value">£{(currExp * sellPrice) / 100}</p>
          </div>
          <div className="text-boxe">
            <h2 className="text-label">Imported Energy Value</h2>
            <p className="text-value">£{(currImp * buyPrice) / 100}</p>
          </div>
          <div className="text-boxe">
            <h2 className="text-label">Profit</h2>
            <p className="text-value">£{profit / 100}</p>
          </div>
      </div>
    </div>
    </div>
  );
}

