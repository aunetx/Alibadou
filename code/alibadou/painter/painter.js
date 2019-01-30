var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');

var painting = document.getElementById('paint');
var paint_style = getComputedStyle(painting);
canvas.width = parseInt(paint_style.getPropertyValue('width'));
canvas.height = parseInt(paint_style.getPropertyValue('height'));

var mouse = {x: 0, y: 0};

canvas.addEventListener('mousemove', function(e) {
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;
}, false);

ctx.lineWidth = 20;
ctx.lineJoin = 'bevel';
ctx.lineCap = 'round';
ctx.strokeStyle = '#000';
ctx.shadowBlur = 20;
ctx.shadowColor = '#000';
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

isOver = 0;

canvas.addEventListener('mousedown', function(e) {
  if ($('#myCanvas:hover').length != 0) {
    isOver = 1;
  } else {
    isOver = 0;
  }
  ctx.beginPath();
  ctx.moveTo(mouse.x, mouse.y);
  canvas.addEventListener('mousemove', onPaint, false);
}, false);

document.addEventListener('mouseup', function() {
  canvas.removeEventListener('mousemove', onPaint, false);
  save(canvas);
  if (isOver == 1) {
    send();
    isOver = 0;
  }
}, false);

canvas.addEventListener('mouseout', function() {
  canvas.removeEventListener('mousemove', onPaint, false);
}, false);

var onPaint = function() {
  ctx.lineTo(mouse.x, mouse.y);
  ctx.stroke();
};

save = function(cv) {
    cv = resize(cv);
    var dataURL = cv.toDataURL();
    $("#exported img").attr('src', dataURL);
    exported_img = dataURL;
  };

resize = function(image) {
    var resizeCanvas = document.getElementById("resize");
    var ctx = resizeCanvas.getContext('2d');
    resizeCanvas.width=28
    resizeCanvas.height=28
    ctx.drawImage(image, 0, 0, 28, 28);
    return resizeCanvas;
  };

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
}

var socket = io();
var delivery = new Delivery(socket);

delivery.on('send.success', function(fileUID){
  console.log("File was successfully sent.");
});

send = function(){
  var file = exported_img;
  file = dataURItoBlob(file);
  delivery.send(file);
};
