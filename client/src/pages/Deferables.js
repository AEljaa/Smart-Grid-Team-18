import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import { Link } from 'react-router-dom';

export default function Home() {
  const [deferableData, setDeferableData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch("http://127.0.0.1:4000/deferables");
        let deferableData = await response.json();

        console.log(deferableData);
        setDeferableData(deferableData); // Update state with fetched data
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
    </div>
  );
}
