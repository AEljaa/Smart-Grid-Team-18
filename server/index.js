const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const router = require('./router');

const app = express(); // create express app

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: false }));


app.use(cors({
    origin: "*",
    credentials: true,
    optionsSuccessStatus: 200

})); // for enabling CORS

app.use ('/',router);

const port = 4000;
const server = app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
