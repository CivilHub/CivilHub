//
// tour.js
// =======

// We create a tour based on the user's current location
// We fetch the capital of the country (depening on the user's IP) from the API.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'tour'],

function ($, _, utils) {

"use strict";

function createTour (template, fn) {
  $.get('/api-locations/capital/', function (data) {

    var rootUrl = "/{}/".replace("{}", data.slug);

    var tour = new Tour({
      steps: [{
        element: "#tour-location-name",
        title: gettext("You are here"),
        content: gettext("Right now you can see the location you are currently in."),
        backdrop: true,
        path: rootUrl
      }, {
        element: "#tour-Summary",
        title: gettext("Summary"),
        content: gettext("Here you can see a list of all of the place's activities."),
        backdrop: true,
        path: rootUrl
      }, {
        element: "#tour-summary-box",
        title: gettext("An activity"),
        content: gettext("In this manner we present the activities to you. Each activity has a category (e.g. Poll, Discussion, Idea etc.). You can view them by simply clicking on text below the title."),
        backdrop: true,
        path: rootUrl
      }, {
        element: "#tour-activity",
        title: gettext("User activity"),
        content: gettext("Here you can see all of the user's activities in this place."),
        backdrop: true,
        placement: "left",
        path: rootUrl
      }, {
        element: "#tour-Blog",
        title: gettext("Blog"),
        content: gettext("Here you can see all of the news connected with the given place. Additionally, you can add your own news, to do so click 'add news' in the right side menu."),
        backdrop: true,
        path: rootUrl + "news/"
      }, {
        element: "#tour-Discussions",
        title: gettext("Discussions"),
        content: gettext("Here you can view or join discussions of a given place. If you feel like adding a new discussion topic you are also free to do so."),
        backdrop: true,
        path: rootUrl + "discussion/"
      }, {
        element: "#tour-Ideas",
        title: gettext("Ideas"),
        content: gettext("View ideas of other users and vote on them. You can also share your creative ideas with others."),
        backdrop: true,
        path: rootUrl + "ideas/"
      }, {
        element: "#tour-votes",
        title: gettext("Voting"),
        content: gettext("Here you can cast your vote. You can view other user's votes by clicking on the number of votes in the bottom part of the window."),
        backdrop: true,
        path: rootUrl + "ideas/"
      }, {
        element: "#tour-Polls",
        title: gettext("Polls"),
        content: gettext("A place where you can view all polls of a given place."),
        backdrop: true,
        path: rootUrl + "polls/"
      }, {
        element: "#tour-Followers",
        title: gettext("Followers"),
        content: gettext("Find out who else is active within this place. Here you can find all of the users that are following this place."),
        backdrop: true,
        path: rootUrl + "followers/"
      }, {
        element: "#tour-map-icon",
        title: gettext("See the map"),
        content: gettext("Jump into the map and see what is happening in your place."),
        placement: "bottom",
        path: rootUrl + "followers/"
      }, {
        element: "",
        title: gettext("Country"),
        content: gettext("Choose the place which you want to alter. Remember that you have the power to change what is happening within your surroundings."),
        path: "/places/",
        orphan: true
      }],
      // storage: false,
      template: template
    });

    tour.init();

    if (_.isFunction(fn)) {
      fn(tour);
    }
  });
}

// We check whether the tour has allready been "killed/finished"

function checkTour () {
  if (Modernizr.localstorage)
    return localStorage.getItem('civilTour');
  else
    return utils.getCookie('civilTour');
}

function initTour () {
  var $tour_init = $('.ac-f-tour');
  var $fake_tour = $('#fake-tour');
  if (!_.isNull(checkTour())) {
    return false;
  }
  if (Modernizr.localstorage) {
    var ls = window.localStorage;
    if (ls.tour_current_step < 4 && ls.getItem('tour_end') == null ) {
      $fake_tour.addClass('when-tour');
      $tour_init.css('z-index', 'inherit');
    } else if (ls.tour_current_step > 4 && ls.getItem('tour_end') == null ) {
      $tour_init.css('z-index', 'inherit');
    }
  }
  return createTour($('#tour-div-tpl').html(),
    function (tour) {
      var $toggle = $($('#tour-button-tpl').html());
      $toggle.appendTo('.main-page-content');
      $toggle.find('#startTour')
        .on('click', function (e) {
          e.preventDefault(e);
          tour.restart();
          tour.start();
          $fake_tour.addClass('when-tour');
          $tour_init.css('z-index', 'inherit');
        });
      $toggle.find('#killTour')
        .on('click', function (e) {
          e.preventDefault();
          if (Modernizr.localstorage) {
            localStorage.setItem('civilTour', true);
            localStorage.removeItem('tour_current_step');
          } else {
            utils.setCookie('civilTour', true, 360);
          }
          $toggle.empty().remove();
        });
    }
  );
}

$(document).ready(initTour);

});
