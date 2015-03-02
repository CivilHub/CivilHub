//
// tour.js
// =======
//
// Tworzy samouczek na podstawie lokalizacji w jakiej znajduje się użytkownik.
// Z API pobieramy stolicę kraju, na jaki wskazuje IP użytkownika.

require(['jquery', 'tour'], function ($) {

  "use strict";

  function createTour () {
    $.get('/api-locations/capital/', function (data) {

      var rootUrl = "/{}/".replace("{}", data.slug);

      var tour = new Tour({
        steps: [{
          element: "#tour-location-name",
          title: gettext("You are here"),
          content: gettext("Right now you can see the location you are currently in."),
          path: rootUrl
        }, {
          element: "#tour-Summary",
          title: gettext("Summary"),
          content: gettext("Here you can see a list of all of the place's activities."),
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
          path: rootUrl + "news/"
        }, {
          element: "#tour-Discussions",
          title: gettext("Discussions"),
          content: gettext("Here you can view or join discussions of a given place. If you feel like adding a new discussion topic you are also free to do so."),
          path: rootUrl + "discussion/"
        }, {
          element: "#tour-Ideas",
          title: gettext("Ideas"),
          content: gettext("View ideas of other users and vote on them. You can also share your creative ideas with others."),
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
          path: rootUrl + "polls/"
        }, {
          element: "#tour-Followers",
          title: gettext("Followers"),
          content: gettext("Find out who else is active within this place. Here you can find all of the users that are following this place."),
          path: rootUrl + "followers/"
        }, {
          element: "#tour-map-icon",
          title: gettext("See the map"),
          content: gettext("Jump into the map and see what is happening in your place."),
          placement: "bottom",
          path: rootUrl + "followers/"
        }, {
          element: "",
          title: gettext("Map"),
          content: gettext("Thanks to the map you can quickly find out what is happening in your neighbourhood."),
          path: "/maps/",
          orphan: true
        }, {
          element: "",
          title: gettext("Country"),
          content: gettext("Choose the place which you want to alter. Remember that you have the power to change what is happening within your surroundings."),
          path: "/places/",
          orphan: true
        }],
        //storage: false,
        template: '<div class="popover" role="tooltip" id="TourDiv"> <div class="arrow"></div> <h3 class="popover-title"></h3> <div class="popover-content"></div> <div class="popover-navigation"> <div class="btn-group"> <button class="btn btn-sm btn-tour" data-role="prev">&laquo; Prev</button>&nbsp; <button class="btn btn-sm btn-tour" data-role="next">Next &raquo;</button> <button class="btn btn-sm btn-tour" data-role="pause-resume" data-pause-text="Pause" data-resume-text="Resume">Pause</button> </div> <button class="btn btn-sm btn-tour" data-role="end">End tour</button> </div> </div>'
      });

      tour.init();

      $('.main-page-content').append('<div class="tourBox"><a href="#" class="btn btn-saveBig" id="startTour"><span class="fa fa-play">Start Tour</span></a></div>');

      $("#startTour").on('click', function (e) {
        e.preventDefault();
        tour.restart();
        tour.start();
      });

      return tour;
    });
  }

  $(document).ready(function () {
    var tour = createTour();
  });

});