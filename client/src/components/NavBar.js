import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css'; // Import the CSS file for styling
import logo from '../assets/logo.png'; // Adjust the path to your logo image

export default function NavBar() {
  return (
    <div className="navBar">
      <img src={logo} className="logo" alt="Logo" />
      <Link to="/" className="navText">Home</Link>
      <Link to="/historic" className="navText">Price & Demand History</Link>
      <Link to="/energy" className="navText">Energy Algorithm Performance</Link>
    </div>
  );
}
