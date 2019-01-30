var express = require('express'),
    app = express();

app.use(express.static(__dirname + '/dots'));

app.listen(3000, function(){
  console.log("Server started")
});
