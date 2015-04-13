//
// features-page.js
// ================

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'fullpagejs'],

  function ($) {

    "use strict";

    function initScroller () {
      $('#fullpage').fullpage({
        verticalCentered: true,
        paddingTop: '69px',
        scrollBar: false,
        anchors: ['slide0', 'slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6', 'slide7', 'slide8', 'slide9', 'slide10', 'slide11'],
        navigation: true,
        navigationPosition: 'right',
        animateAnchor: true,
        css3: true,
        keepHistory: false,
        menu: '#menuSection',

        // turns off the whole script at this resolution
        responsive: 650,

        afterRender: function () {
          $.fn.fullpage.reBuild();
        },

        afterLoad: function (anchorLink, index) {
          if (index == 1 || anchorLink == 'slide1'){
            $('.menuBlock').addClass('hide');
          } else {
            $('.menuBlock').removeClass('hide');
          }
        },

        onLeave: function (index, nextIndex, direction) {
          $.fn.fullpage.reBuild();

          if (index >= 3 && nextIndex <= 9 && direction == 'up'){
            $('#menuSection').removeClass('hide');
            $('.menuBlock').removeClass('hide');
          } else if (index >= 3 && nextIndex <= 9 && direction == 'down'){
            $('#menuSection').removeClass('hide');
            $('.menuBlock').removeClass('hide');
          } else {
            $('.menuBlock').addClass('hide');
            $('#menuSection').addClass('hide');
          }

          if (index == 4 && direction == 'up'){
            $('#menuSection').addClass('hide');
            $('.menuBlock').addClass('hide');
          }

          if ($(window).width() > 650) {
            if (index == 1 && direction == 'down') {
              $('#staticImg .imgsContainer').removeClass('jump');
              $('#staticImg').addClass('moveDown imgSec');
            }
            else if (index == 2 && direction == 'up'){
              $('#staticImg .imgsContainer').addClass('jump');
              $('#staticImg').removeClass('imgSec');
            } else if (index == 2 && direction == 'down'){
              $('#staticImg').addClass('imgSec');
            }

            $('#staticImg').toggleClass('moveDown', nextIndex == 2);
            $('#staticImg').toggleClass('moveUp', index == 1 && direction == 'up');
          }

        }
      });
    }

    $(document).ready(function () {
      window.setTimeout(function () {
        initScroller();
      }, 1000);

      setTimeout(function () {
        $('.features-preloader').addClass('hide');
      }, 1000);

    });

    $(document).trigger('load');

  });
});
