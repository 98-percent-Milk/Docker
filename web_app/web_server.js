'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const { check, validationResult } = require('express-validator');
const request = require('request-promise');
// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();

const urlencodedParser = bodyParser.urlencoded({ extended: false })
app.set('view engine', 'ejs');
let data = {}

app.get('', (req, res) => {
    res.render('index')
})

app.get('/validate', (req, res) => {
    res.render('validate')
})

app.get('/temperature', (req, res) => {
    res.render('temperature')
})

app.post('/validate', urlencodedParser, [
    check('username', 'This username must me 3+ characters long')
        .exists()
        .isLength({ min: 3 }),
], (req, res) => {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
        const alert = errors.array()
        res.render('validate', {
            alert
        })
    }
    request({
        method: "POST",
        uri: "http://localhost:8100/login/authenticate",
        headers: { "content-type": "application/json" },
        body: {
            username: req.body.username,
            password: req.body.password,
        },
        json: true,
    })
        .then(function (body) {
            if (body.statusCode == 201) {
                console.log("Welcome Admin")
                res.render("temperature")
            } else {
                console.log("Not Welcome")
                res.render('index')
            }
        })
        .catch(function (err) {
            console.log(err.name, err.statusCode);
            res.render('index')
        })
})

app.post('/temperature', urlencodedParser, (req, res) => {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
        const alert = errors.array()
        res.render('validate', {
            alert
        })
    }
    request({
        method: "POST",
        uri: "http://localhost:8090/readings/temperature",
        headers: { "content-type": "application/json" },
        body: {
            temperature: req.body.temperature,
        },
        json: true,
    })
        .then(function (body) {
            if (body.statusCode == 201) {
                console.log("Temperature Saved")
                res.render("temperature")
            } else {
                console.log("Temperature Not Saved")
                res.render('index')
            }
        })
        .catch(function (err) {
            console.log(err.name, err.statusCode);
            res.render('index')
        })
})

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);