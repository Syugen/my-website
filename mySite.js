'use strict';

var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var http = require("http");
var server = http.createServer(app);

app.use(express.static(__dirname + '/assets'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.set('views', __dirname);
app.set('view engine', 'html');

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/public/index.html");
});

app.get("/project", function(req, res) {
    res.sendFile(__dirname + "/public/project.html");
});

app.get("/project/:name", function(req, res) {
    var path = __dirname + "/public/projects/" + req.params.name + ".html";
    var fs = require('fs');
    if (fs.existsSync(path)) {
        res.sendFile(path);
    } else {
        res.status(404).send("DNE (For a better 404 page, constructing)");
    }
});

app.get("/interest", function(req, res) {
    res.send("Constructing");
});

app.get("*", function(req, res) {
    res.status(404).send("404 (For a better 404 page, constructing)");
});

server.listen(3003, function(request, response) {
    console.log("Running on 127.0.0.1:%s", server.address().port);
});
