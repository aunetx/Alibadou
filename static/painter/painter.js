//  Canvas init

var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');

var painting = document.getElementById('paint');
var paint_style = getComputedStyle(painting);
canvas.width = parseInt(paint_style.getPropertyValue('width'));
canvas.height = parseInt(paint_style.getPropertyValue('height'));

var mouse = {x: 0, y: 0};
var touch = {x: 0, y: 0};

canvas.addEventListener('mousemove', function(e) {
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;
}, false);

canvas.addEventListener('touchmove', function(e) {
  touch.x = e.changedTouches[0].pageX-e.changedTouches[0].target.offsetLeft;
  touch.y = e.changedTouches[0].pageY-e.changedTouches[0].target.offsetTop;
  event.preventDefault();
}, false);

ctx.lineWidth = 25;
ctx.lineJoin = 'bevel';
ctx.lineCap = 'round';
ctx.strokeStyle = '#00000050';
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.imageSmoothingEnabled = false;

//  Canvas events

canvas.addEventListener('mousedown', function(e) {
  ctx.beginPath();
  ctx.moveTo(mouse.x, mouse.y);
  canvas.addEventListener('mousemove', onPaint, false);
}, false);

document.addEventListener('mouseup', function() {
  canvas.removeEventListener('mousemove', onPaint, false);
  save(canvas);
}, false);

canvas.addEventListener('mouseout', function() {
  canvas.removeEventListener('mousemove', onPaint, false);
}, false);

canvas.addEventListener('touchstart', function(e) {
  console.log('ok');
  ctx.moveTo(touch.x, touch.y);
  ctx.beginPath();
  canvas.addEventListener('touchmove', onPaintTouch, false);
}, false);

document.addEventListener('touchend', function() {
  canvas.removeEventListener('touchmove', onPaintTouch, false);
  save(canvas);
}, false);

canvas.addEventListener('touchleave', function() {
  canvas.removeEventListener('touchmove', onPaintTouch, false);
}, false);

//  Canvas functions

sendButton = document.getElementById('send');

onPaint = function() {
  ctx.lineTo(mouse.x, mouse.y);
  ctx.stroke();
};

onPaintTouch = function() {
  ctx.lineTo(touch.x, touch.y);
  ctx.stroke();
};

reset = function() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    $('#prediction').text('Réessayez !');
    option = basic_option;
    myChart.setOption(option);
  };

save = function(cv) {
    cv = resize(cv);
    var dataURL = cv.toDataURL();
    $("#exported img").attr('src', dataURL);
    exported_img = dataURL;
  };

resize = function(image) {
    var resizeCanvas = document.getElementById("resize");
    var middleCanvas = document.getElementById("middleCanvas");
    var mdCtx = middleCanvas.getContext('2d');
    middleCanvas.width=280
    middleCanvas.height=280
    mdCtx.filter = 'blur(4px) contrast(140%)';
    mdCtx.drawImage(image, 0, 0, 280, 280);
    var ctx = resizeCanvas.getContext('2d');
    resizeCanvas.width=28
    resizeCanvas.height=28
    ctx.drawImage(middleCanvas, 0, 0, 28, 28);
    return resizeCanvas;
  };

//  Sockets

function dataURItoBlob(dataURI) {
  var byteString = atob(dataURI.split(',')[1]);

  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

  var arrayBuffer = new ArrayBuffer(byteString.length);
  var _ia = new Uint8Array(arrayBuffer);
  for (var i = 0; i < byteString.length; i++) {
    _ia[i] = byteString.charCodeAt(i);
  }

  var dataView = new DataView(arrayBuffer);
  var blob = new Blob([dataView], { type: mimeString });
  return blob;
};

send = function() {
  var file = exported_img;
  file = dataURItoBlob(file);
  delivery.send(file);
  sentSize = file.size;
}

var socket = io();
var delivery = new Delivery(socket);

delivery.on('send.success', function(fileUID){
  console.log("File was successfully sent.");
  sendButton.disabled = true;
});

socket.on('computing', function() {
  console.log('Starting computing');
  $('#progress').toggleClass('hidden');
  $('#prediction').toggleClass('hidden');
  sendButton.disabled = false;
});

socket.on('message', function(msg) {
  var data = msg['data'];
  var size = msg['size'];
  var json_message = JSON.parse(data);
  prediction = json_message['prediction'];
  accuracy = json_message['accuracy'];
  accuracy.forEach(function(item, index, array) {
    accuracy[index] = parseFloat(item).toFixed(2);
    if (accuracy[index] > 1) {
      accuracy[index] = 1.00;
    }
  });
  if (sentSize == size) {
    console.log("Taille correspondante.")
  } else {
    console.log("Erreur : taille non correspondante.")
  }
  console.log(accuracy);
  $('#progress').toggleClass('hidden');
  $('#prediction').toggleClass('hidden');
  $('#prediction').text(' '+prediction);
  updateChart();
});

//  Charts

myChart = echarts.init(document.getElementById('chart'), null, {renderer: 'svg'});
var basic_option = {
  title: {
    show: false
  },
  tooltip: {},
  xAxis: {
    data: ["0","1","2","3","4","5","6","7","8","9"],
    name: 'nombre',
    axisLine: {
      lineStyle: {
        color: "#abb4ba"
      }
    },
    axisLabel: {
      textStyle: {
        color: "#abb4ba"
      }
    }
  },
  yAxis: {
    name: 'Précision de\nla prédiction',
    min: 0,
    max: 1,
    axisLine: {
      lineStyle: {
        color: "#abb4ba"
      }
    },
    axisLabel: {
      textStyle: {
        color: "#abb4ba"
      }
    }
  },
  series: [{
    name: 'accuracy',
    type: 'bar',
    data: [0,0,0,0,0,0,0,0,0,0]
  }],
  color: ['#CB4D4D']
}
option = basic_option;
myChart.setOption(option);
updateChart = function() {
  var option = {
    title: {
      show: false
    },
    tooltip: {},
    xAxis: {
      data: ["0","1","2","3","4","5","6","7","8","9"],
      name: 'nombre'
    },
    yAxis: {
      name: 'Précision de\nla prédiction'
    },
    series: [{
      name: 'accuracy',
      type: 'bar',
      data: accuracy
    }],
    color: ['#CB4D4D']
  }
  myChart.setOption(option);
}
