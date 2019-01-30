$(document).ready(function() {
  var croquis = new Croquis();
  croquis.setCanvasSize(280, 280);
  var domElement = croquis.getDOMElement();

  croquis.addLayer();
  croquis.fillLayer('black');

  croquis.lockHistory(); //not using history
  var brush = new Croquis.Brush();
  brush.setSize(21);
  brush.setColor('#fff');
  brush.setSpacing(0.05);
  brush.setFlow(0.39);
  brush.setNormalSpread(0.48)
  croquis.setTool(brush);
  croquis.setToolStabilizeLevel(1); //not using stabilizer

  var image = document.getElementById('brush');
  image.className = 'brush png';
  brush.setImage(image);

  // croquis dom element
  document.body.appendChild(croquis.getDOMElement());

  // mouse event
  document.addEventListener('mousedown', function (e) {
      croquis.down(e.clientX, e.clientY);
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
  });
  function onMouseMove(e) {
      croquis.move(e.clientX, e.clientY);
  }
  function onMouseUp(e) {
      croquis.up(e.clientX, e.clientY);
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
  }
  var img = $("#showed_img");
  //document.addEventListener('mousemove', to_image());
  $("body").mousemove(to_image());
});

function to_image(){
  console.log('move')
  canvas = document.getElementsByClassName('croquis-layer-canvas')
  canvas = canvas[0]
  //$(img).attr("src", canvas.toDataURL());
}
