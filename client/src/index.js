import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Energy from './pages/Energy';
import Historic from './pages/Historic';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/energy" element={<Energy />} />
        <Route path="/historic" element={<Historic />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

reportWebVitals();
