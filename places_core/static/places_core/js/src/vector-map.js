//
// vector-map.js
// =============
// 
// Skrypt odpowiadający za prawidłowe wyświetlanie vector-map

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'hammer',
           'jeasing',
           'jmousewheel',
           'mapplic'],
           
  function ($) {
      
    "use strict";
    
    $('#mapplic').mapplic({
      source: '/static/places_core/includes/mapplic/world.json',
      height: '100%',
      animate: true,
      sidebar: true,
      minimap: false,
      locations: true,
      deeplinking: true,
      fullscreen: false,
      hovertip: false,
      developer: false,
      maxscale: 4,
      zoom: true 
    });

    $(window).load(function() {

      //$('.mapplic-sidebar').prepend('<div class="mapplicCountry"><p class="mappCountry">' + gettext("Country") + '</p><p>' + gettext("Search by location") + '<span class="fa fa-caret-down"></span></p></div>');

      $('.mapplicCountry').click(function(){
        $('.mapplic-search-form, .mapplic-list-container').toggle();
      });

      $('.mapplic-layer a').addClass('jump-marker');

    });

    $('.clear').hide();

    $(document).trigger('load');
      
  });
});
