'use strict';

var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var http = require("http");
var server = http.createServer(app);

//var video = require("./routes/video");
//var user = require("./routes/user");
//var api = require("./routes/api");

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

app.get("/interest", function(req, res) {
    res.send("Constructing");
});

app.get("*", function(req, res) {
    res.status(404).send("404");
});

server.listen(3003, function(request, response) {
    console.log("Running on 127.0.0.1:%s", server.address().port);
});
