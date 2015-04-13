//
// search-toggle.js
// ==============
//

require(['jquery'], function ($) {

  "use strict";

/*  $('#search-bar-icon').click(function(e){
    e.preventDefault();
    $('.search-bar-box').animate({width: 'toggle'},200);
  });*/

  $('#search-bar-icon').on('click', function(){
    if($('.search-bar-box').hasClass('hidden')){
      $('.search-bar-box').removeClass('hidden').animate({width: '100%'}, 200);
    } else {
      $('.search-bar-box').addClass('hidden').animate({width: '0%'}, 200);
    }

  });

});