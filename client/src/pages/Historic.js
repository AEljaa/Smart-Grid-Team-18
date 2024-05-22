import React from 'react';
import NavBar from '../components/NavBar';
import { Line } from 'react-chartjs-2';
import './Historic.css';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  } from 'chart.js';
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

export default function Historic() {
  // Sample data (replace this with your actual data from the JSON file)
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Price Per Watt',
        data: [0.20, 0.45, 0.28, 0.80, 0.99, 0.43],
        fill: true,
        backgroundColor: '#FFFFFF',
        borderColor: '#FFFFFF',
      },
    ],
  };

  const options = {
    maintainAspectRatio: false,
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Price Per Watt (£)', // Label for the y-axis
                color: '#FFFFFF',
                font: {
                    size: 16,
                    weight: 'bold'
                }
            }
        },
        x: {
            title: {
                display: true,
                text: 'Month', // Label for the x-axis
                color: '#FFFFFF',
                font: {
                    size: 16,
                    weight: 'bold'
                }
            }
        }
    },
};


  return (
    <div className="container">
      <NavBar />
      <div className="content">
        <h1 className="title">Price Per Watt History</h1>
        <div className="chart-container">
          <Line data={data} options={options} />
        </div>
      </div>
    </div>
  );
}
