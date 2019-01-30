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

canvas.addEventListener('mousedown', function(e) {
  ctx.beginPath();
  ctx.moveTo(mouse.x, mouse.y);
  canvas.addEventListener('mousemove', onPaint, false);
  save(canvas);
}, false);

canvas.addEventListener('mouseup', function() {
  canvas.removeEventListener('mousemove', onPaint, false);
  save(canvas);
}, false);

canvas.addEventListener('mouseout', function() {
  canvas.removeEventListener('mousemove', onPaint, false);
  save(canvas);
}, false);

var onPaint = function() {
  ctx.lineTo(mouse.x, mouse.y);
  ctx.stroke();
  save(canvas);
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

save(canvas);

var socket = io.connect();

send = function() {
  var file = exported_img;
  var stream = ss.createStream();

  ss(socket).emit('file', stream);
};
