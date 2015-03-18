//
// brief.js
// ==============

// Zmiana obrazka z miastami w slide9 na brief.html(article). Dopisać zmianę tak aby moża było wykorzystać ten slider w innych celach.

require(['jquery'], function ($) {

  "use strict";

  $('.bg-control').click(function(){
  	event.preventDefault();
  	$('#brief-slider-img').attr('src','/static/places_core/img/brief/pl_slide_9.png');
  });

});