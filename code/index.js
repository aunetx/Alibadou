const express = require('express');
const app = express();

var firstArg = 'misere'

app.get('/', (req, res) => {
  var spawn = require('child_process').spawn,
  py = spawn('python', ['./snn.py', firstArg]),
  dataString = '';

  py.stdout.on('data', (data) => {
    dataString = dataString + data.toString();
  });
  py.stdout.on('end', () => {
    res.render('main.ejs', {sortie: dataString});
    console.log('tick')
  });
});

app.listen(3000, () => {
  console.log('server started');
});

// Copyright aunetx 2018
