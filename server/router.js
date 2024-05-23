// router.js
const express = require('express');
const router = express.Router();


// Route to fetch and send sun data
router.get('/sun', async (req, res) => {
    try {
        const response = await fetch('https://icelec50015.azurewebsites.net/sun');
        const sunData = await response.json();
        res.json(sunData);
        console.log(sunData);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while fetching sun data' });
    }
});

// Route to fetch and send price data
router.get('/price', async (req, res) => {
    try {
        const response = await fetch('https://icelec50015.azurewebsites.net/price');
        const priceData = await response.json();
        res.json(priceData);
        console.log(priceData);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while fetching price data' });
    }
});

router.get('/demand', async (req, res) => {
    try {
        const response = await fetch('https://icelec50015.azurewebsites.net/demand');
        const demandData = await response.json();
        res.json(demandData);
        console.log(demandData);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while fetching demand data' });
    }
});

module.exports = router;
