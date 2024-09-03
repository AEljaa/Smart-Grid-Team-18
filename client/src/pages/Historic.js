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
  const [chartCapData, setChartCapData] = useState(0);
  const [chartGridData, setChartGridData] = useState(0);
  useEffect(() => {
    const fetchData = async () => {
      try {

        let startTime = performance.now();
        let response = await fetch("http://127.0.0.1:4000/yesterday");
        let yesterdayData = await response.json();
        response = await fetch("http://127.0.0.1:4000/forward_cap_graph_data");
        let capData = await response.json();

        response = await fetch("http://127.0.0.1:4000/forward_grid_graph_data")
        let gridData = await response.json();

        console.log(gridData);
        
        let labels = yesterdayData.tick;
         const GridData ={
          labels: labels,
          datasets: [
            {
              label: 'Energy Imported (+ve), Energy Exported (-ve) (Joules)',
              data: gridData,
              fill: true,
              backgroundColor: 'rgba(153,102,255,0.4)',
              borderColor: 'rgba(153,102,255,1)',
            }
          ] 
        };


          const CapData ={
          labels: labels,
          datasets: [
            {
              label: 'Stored Energy in Capacitor (Joules)',
              data: capData,
              fill: true,
              backgroundColor: 'rgba(255, 99, 132, 0.4)',
              borderColor: 'rgba(255, 99, 132, 1)',
            }
          ] 
        };

        const data ={
          labels: labels,
          datasets: [
            {
              label: 'External Buy Price Per Joule (pence)',
              data: yesterdayData.buyHist,
              fill: true,
              backgroundColor: 'rgba(75,192,192,0.4)',
              borderColor: 'rgba(75,192,192,1)',
            },
            {
              label: 'External Sell Price Per Joule (pence)',
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
        setChartCapData(CapData);
        setChartGridData(GridData);
        let endTime = performance.now();
        console.log(`Duration: ${endTime - startTime}ms`);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); //Cap data changes every 5 secs so refresh graph
    return () => clearInterval(interval); // Cleanup interval on component unmount
  
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
                    size: 20,
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
                    size: 25,
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
    <div className="chart-container-wrapper">
          <div className="chart-container">
              {chartData ? <Line data={chartData} options={options} /> : <p>Loading...</p>}
          </div>
          <div className="chart-container">
              {chartCapData ? <Line data={chartCapData} options={options} /> : <p>Loading...</p>}
        </div>
          <div className="chart-container">
              {chartGridData ? <Line data={chartGridData} options={options} /> : <p>Loading...</p>}
        </div>
      </div>
    </div>
  </div>
);
}
