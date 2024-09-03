
import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';

export default function Home() {
  const [deferableData, setDeferableData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch("http://127.0.0.1:4000/curr_deferables");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        let data = await response.json();
        console.log("Fetched Data:", data);

        const deferableArray = Object.entries(data)
          .filter(([key, value]) => key !== 'ourtick')
          .map(([key, value]) => ({ id: key, ...value }));

        setDeferableData(deferableArray);
      } catch (error) {
        console.error("Fetch error:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const keys = deferableData.length ? Object.keys(deferableData[0]) : [];

  return (
    <div className="container">
      <NavBar />
      <h1>Deferable List</h1>
      <div className="deferable-list">
        {deferableData.length > 0 ? (
          <table>
            <thead>
              <tr>
                {keys.map((key, idx) => (
                  <th key={idx}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {deferableData.map((item, idx) => (
                <tr key={idx}>
                  {keys.map((key, idx) => (
                    <td key={idx}>{item[key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No deferables available</p>
        )}
      </div>
    </div>
  );
}
