const express = require('express')
    , app = express()
    , http = require('http').Server(app)
    , io = require('socket.io')(http)
    , dl = require('delivery')
    , fs = require('fs');

app.use(express.static(__dirname + '/'));

app.get('/delivery.js', (req, res, next) => {
    return res.sendFile(__dirname + '/node_modules/delivery/lib/client/delivery.js');
});

io.sockets.on('connection', function(socket) {
  console.log('Connection to socket.io active.')
  var delivery = dl.listen(socket);
  delivery.on('receive.success', function(file) {
    var params = file.params;
    file["name"] = 'temp/result.png';
    fs.writeFile(file.name, file.buffer, function(err) {
      if (err) {
        console.log('File could not be saved.');
      } else {
        console.log('Temp image saved');
      };
    });
  });
});

//var spawn = require('child_process').spawn,
//  py = spawn('python', ['./snn.py', firstArg]),
//  dataString = '';
//
//  py.stdout.on('data', (data) => {
//    dataString = dataString + data.toString();
//  });
//  py.stdout.on('end', () => {
//    res.render('main.ejs', {sortie: dataString});
//    console.log('tick')
//  });

http.listen(3000, () => {
    console.log('Server started on localhost:3000');
});
