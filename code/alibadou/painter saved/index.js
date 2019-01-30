const express = require('express'),
      app = express(),
      http = require('http').Server(app),
      io = require('socket.io')(http),
      ss = require('socket.io-stream'),
      path = require('path'),
      fs = require('fs');

app.use(express.static(__dirname + '/'));

io.on('connection', function(socket){
  console.log('connected');
});

io.on('connection', function(socket){
  ss(socket).on('file', function(stream) {
    console.log(stream);
    stream.pipe(fs.createWriteStream(__dirname + '/' + 'filename.png'));
  });
});

http.listen(3000, function(){
  console.log("Server started")
});
