const express = require('express')
    , app = express()
    , http = require('http').Server(app)
    , io = require('socket.io')(http)
    , fs = require('fs')
    , util = require('util')
    , dl = require('delivery')
    , spawn = require('child_process').spawn;

app.use(express.static(__dirname + '/'));

app.get('/delivery.js', (req, res, next) => {
    return res.sendFile(__dirname + '/node_modules/delivery/lib/client/delivery.js');
});

function getDateTime() {
  var date = new Date()
    , year = date.getFullYear()
    , month = date.getMonth() + 1
    , day = date.getDate()
    , hour = date.getHours()
    , min = date.getMinutes()
    , s = date.getSeconds()
    , ms = date.getMilliseconds();
  return day + "-" + month + "-" + year + " " + hour + "h " + min + "min " + s + "s " + ms + "ms";
}

authorizedPage = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15 ];
var log = true;

if (log) {
  var logPath = __dirname + '/logs/' + getDateTime() + '.log'
    , log_file = fs.createWriteStream(logPath, {flags : 'w'})
    , log_stdout = process.stdout;
  console.log = function(d) {
    log_file.write(getDateTime() + " : " + util.format(d) + '\n');
    log_stdout.write(getDateTime() + " : " + util.format(d) + '\n');
  };
  console.error = function(d) {
    return new Promise(function(errorWrote) {
      log_file.write(getDateTime() + " : " + util.format(d) + '\n');
      log_stdout.write(getDateTime() + " : " + util.format(d) + '\n');
      errorWrote(true);
    })
  };
}

function fileRead(fl, ext, id) {
  try {
    out = fs.readFileSync(fl + ext, 'utf8');
  } catch (err) {
    error = true;
    console.log('ERROR! Client : ' + id);
    console.error(err);
    setTimeout(function () {
      process.exit();
    }, 100)
  }
  return out
}

function writeClientFile(type) {
  var nbClients;
  fs.readFile('logs/clients', function read(err, data) {
    if (err) {
        throw err;
    }
    nbClients = parseInt(data, 10);
    if (type == 'connection') {
      nbClients += 1;
    } else if (type == 'disconnect') {
      nbClients -= 1;
    }
    fs.writeFile('logs/clients', nbClients, (err) => {
      if (err) {
        console.error(err)
        return
      }
    })
  });
}

io.sockets.on('connection', function(socket) {
  error = false;
  var socketId = socket.id;
  var clientIp = socket.request.connection.remoteAddress;
  if (clientIp.substr(0, 7) == "::ffff:") {
    clientIp = clientIp.substr(7);
  }
  console.log('Real-time connection up with '+clientIp+', id = '+socketId);
  socket.emit('connected');

  writeClientFile('connection');

  socket.on('goToPage', function(page){
    console.log(page);
    if (authorizedPage.includes(page)) {
      console.log('Authorized access for client ' + socketId);
      page = 'rawHtml/' + page;

      var jsonPage = fileRead(page, '.json', socketId);
      jsonPage = JSON.parse(jsonPage);
      jsonPage.content = fileRead(page, '.html', socketId);

      if (!error) {
        socket.emit('page', jsonPage);
        console.log('Page sent to client ' + socketId)
      }
    }
  });

  socket.on('disconnect', function() {
    console.log('Client déconnecté : ' + socketId);
    writeClientFile('disconnect');
  });

  var delivery = dl.listen(socket);
  delivery.on('receive.success', function(file) {
    var params = file.params;
    file["name"] = 'painter/temp/result.png';
    fs.writeFile(file.name, file.buffer, function(err) {
      if (err) {
        console.log('ERROR : File could not be saved for client ' + socketId);
        console.log('Path : ' + file.name);
      } else {
        console.log('Temp image saved for client ' + socketId);
        var py = spawn('python', ['painter/loulou/run.py', 'painter/loulou/blended/5L 400-200-100 0.03.npy', 'painter/temp/result.png']);
        socket.emit('computing');
        py.stdout.on('data', (data) => {
          var msg = {'data': data.toString(), 'size': file.size};
          socket.emit('message', msg);
          console.log('Image computing done for client ' + socketId);
        });
      };
    });
  });
});

http.listen(3000, () => {
    console.log('Server started on port 3000');
});
