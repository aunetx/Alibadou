$(document).ready(function() {
	$(".g a").on('click', function(event) {
    event.preventDefault();
    var hash = this.getAttribute("href");
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 800, function(){
      window.location.hash = hash;
    });
  });
});

window.onscroll = function() {
	var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
	if (scrollTop > window.innerHeight-53) {
		$( "nav" ).addClass( "blacked" );
	} else {
		$( "nav" ).removeClass( "blacked" );
	}
}
