import React from 'react';
import NavBar from '../components/NavBar';
import { Line } from 'react-chartjs-2'; //Followed guide here https://codesandbox.io/p/devbox/reactchartjs-react-chartjs-2-default-1695r?embed=1&file=%2FApp.tsx
import './Historic.css';
import{ useState, useEffect } from 'react';
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
  const [chartData, setChartData] = useState(0);
  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch("http://127.0.0.1:4000/yesterday");
        let yesterdayData = await response.json();
        console.log(yesterdayData);
        let labels = yesterdayData.tick;
        const data ={
          labels: labels,
          datasets: [
            {
              label: 'External Buy Price Per Watt (pence)',
              data: yesterdayData.buyHist,
              fill: true,
              backgroundColor: 'rgba(75,192,192,0.4)',
              borderColor: 'rgba(75,192,192,1)',
            },
            {
              label: 'External Sell Price Per Watt (pence)',
              data: yesterdayData.sellHist,
              fill: true,
              backgroundColor: 'rgba(153,102,255,0.4)',
              borderColor: 'rgba(153,102,255,1)',
            },
            {
              label: 'Demand',
              data: yesterdayData.demandHist,
              fill: true,
              backgroundColor: 'rgba(255, 99, 132, 0.4)',
              borderColor: 'rgba(255, 99, 132, 1)',
            }
              
          ] 
        };
        setChartData(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  const options = {
    maintainAspectRatio: false,
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Values',
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
                text: 'Time (Ticks)',
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
          <h1 className="title">History Data</h1>
          <div className="chart-container">
              {chartData ? <Line data={chartData} options={options} /> : <p>Loading...</p>}
          </div>
      </div>
  </div>
);
}
