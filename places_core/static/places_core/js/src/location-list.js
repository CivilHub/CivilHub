//
// location-list.js
// ================

// Location browser in a form of a vector map.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/locations/location-list/col-view',
           'js/modules/locations/follow-button',
           'vector',
           'worldmap',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/locations/simple-autocomplete'],

  function ($, ColView, fb) {

    // openPlaceholderWindow
    // ---------------------
    // Helper function: opens the main window that stores lists
    // ---------------------------------------------------------------------
    var openPlaceholderWindow = function () {
      $('#list-placeholder')
        .fadeIn('slow')
        .find('.placeholder-close')
        .on('click', function (e) {
          e.preventDefault();
          closePlaceholderWindow();
        });
    };

    // openPlaceholderWindow
    // ---------------------
    // Helper function: closes the main window that contains the lists
    // ---------------------------------------------------------------------
    var closePlaceholderWindow = function () {
      $('#list-placeholder').fadeOut('slow', function () {
        $(this).find('.placeholder-content').empty();
        delete window.activeSublist;
      });
    };

    // openList
    // --------
    // The proper function that opens the first "level" of the list or displays
    // an alert if in the database there is no country with that code
    //
    // @param event { jQuery.event || vectorMap.event} a caught click
    // @param code  { string } A two-lettered code country (case insensitive)
    // ---------------------------------------------------------------------
    var openList = function (event, code) {
      // If there is a list that is already active for a country, do not
      // open a new window
      if (window.activeSublist !== undefined && window.activeSublist) {
        return false;
      }
      // We check whether the country is already in the database. If yes
      // we open a list.
      $.get('/api-locations/countries/?code=' + code, function (resp) {
        if (resp.length) {
          // We MUST pass an empty table as the first argument - Backbone
          // always treats the first argument as a collection, which here,
          // leads to errors
          var locationList = new ColView([], resp[0].location, 1);
          window.activeSublist = locationList;
          locationList.on('destroyed', function () {
            closePlaceholderWindow();
          });
          openPlaceholderWindow();
        } else {
          // TODO: something needs to be shown here.
          // alert("There is no such place");
          var dialog = $('#no-place-dialog');
          dialog.fadeIn();
          dialog
            .find('.placeholder-close')
            .on('click', function (e) {
              dialog.fadeOut();
            });
        }
      });
    };

    var showPopup = function (countryCode) {
      $.get('/api-locations/locations/?code=' + countryCode, function (resp) {
        if (resp) {
          $('#countryName').text(gettext('Go to') + ' ' + resp.name);
          $('#countryName').attr('href', '/' + resp.slug);

          var followButton = $('#follow-button');
          var targetID = resp.id;
          var name = resp.name;
          followButton.attr('data-target', targetID);

          if (resp.followed) {
            followButton
              .addClass('btn-unfollow-location')
              .text(gettext('Stop following') + ' ' + name);
          } else {
            followButton
              .addClass('btn-follow-location')
              .text(gettext('Follow') + ' ' + name);
          }

          followButton.on('click', function (e) {
            var $this = $(e.currentTarget);
            fb.followRequest($this.attr('data-target'), function (response) {
              var txt = response.following ? gettext('Stop following')
                                           : gettext('Follow');
              $this.text(txt + ' ' + name)
                .toggleClass('btn-follow-location')
                .toggleClass('btn-unfollow-location');
            }, $this);
          });

        } else {
          alert("There is no such place");
        }
      });
    };

    // Mapa
    // ----
    // Displays a vector map and launches a certain list after a click
    // ---------------------------------------------------------------------
    $('#vector-map').vectorMap({

      map: 'world_mill_en',

      backgroundColor: 'transparent',

      onRegionClick: function (element, code, region) {
        openList(element, code);
        showPopup(code);
      },

      regionStyle: {
        initial: {
          fill: '#8D8D8D',
          "fill-opacity": 1,
          stroke: 'none',
          "stroke-width": 0,
          "stroke-opacity": 1
        },
        hover: {
          fill: '#0082FC',
          "fill-opacity": 0.8
        }
      }

    });

    // Custom Events
    // -------------
    // Opens a location list after the name of the country is clicked
    // ---------------------------------------------------------------------
    $('.country-entry').on('click', function (e) {
      e.preventDefault();
      var countryCode = $(this).attr('data-code');
      openList(e, countryCode);
      // We check whether the country is already in the database. If yes, we open a list
      showPopup(countryCode);
    });

    $(document).trigger('load');

  });
});
