'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const { check, validationResult } = require('express-validator');
const request = require('request-promise');
const mysql = require('mysql')
const crypto = require('crypto');
// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();

const urlencodedParser = bodyParser.urlencoded({ extended: false })
app.set('view engine', 'ejs');

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
        uri: "http://authenticate:8100/login/authenticate",
        headers: { 'content-type': 'application/json' },
        body: {
            username: req.body.username,
            password: req.body.password,
        },
        json: true,
    }, function (error, response) {
        if (response.statusCode == 201) {
            res.render('temperature')
            console.log("testing")
        } else {
            res.render('index')
        }
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
    var con = mysql.createConnection({
        host: "storage",
        user: "root",
        password: "MyNewPass1!",
        database: "events"
    });

    con.connect(function (err) {
        if (err) throw err;
        console.log("connects to db container");
        var sql = `INSERT INTO events (temperature) VALUES ("${crypto.randomUUID()},${req.body.temperature}")`;
        con.query(sql, function (err, result) {
            if (err) {
                con.end(function (err) { })
                console.log("didnt work");
            } else {
                res.render('temperature')
                console.log("added thing to database");
            }
        })
    })
})
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`)
