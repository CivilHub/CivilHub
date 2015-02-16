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
          title: "Jesteś tutaj",
          content: "Widzisz właśnie nazwę lokalizacji, w której aktualnie się znajdujesz.",
          path: rootUrl
        }, {
          element: "#tour-Summary",
          title: "Podsumowanie",
          content: "W tym miejscu możesz obserwować wszystkie aktywności dla tej lokalizacji.",
          path: rootUrl
        }, {
          element: "#tour-summary-box",
          title: "Aktywność",
          content: "Aktywności przedstawiamy tobie w taki oto sposób. Każda aktywność posiada własną kategorię (m.in. Ankieta, Dyskusja, Pomysł itp). Możesz do nich przechodzić bezpośrednio klikając w treść znajdującą się pod tytułem.",
          backdrop: true,
          path: rootUrl
        }, {
          element: "#tour-activity",
          title: "Aktywność użytkowników",
          content: "W tym miejscu znajdują się wszytskie aktywności jakie dany użytkownik wykonał dla tego miejsca.",
          backdrop: true,
          path: rootUrl
        }, {
          element: "#tour-Blog",
          title: "Blog",
          content: "Znajdziesz tutaj wszystkie aktualności związane z tą lokalizacją. Ponadto możesz tworzyć własne aktualności wybierając w panelu bocznym dodaj aktualność. ",
          path: rootUrl + "news/"
        }, {
          element: "#tour-Discussions",
          title: "Dyskusje",
          content: "Możesz przglądać dyskusje poruszone w tej lokalizacji bądź samemy dołączyć do takiej dyskusji. Tworzenie nowych dyskusji jest również w twojej mocy.",
          path: rootUrl + "discussion/"
        }, {
          element: "#tour-Ideas",
          title: "Pomysły",
          content: "Przeglądaj pomysły użytkowników i oceniaj je. Dziel się również swoimy ciekawymi pomysłami.",
          path: rootUrl + "ideas/"
        }, {
          element: "#tour-votes",
          title: "Głosowanie",
          content: "Tu oddajesz swój głos. Możesz przeglądać głosy innych klikająć w ilość głosów w dolnej części okienka.",
          backdrop: true,
          path: rootUrl + "ideas/"          
        }, {
          element: "#tour-Polls",
          title: "Ankiety",
          content: "Miejsce, w którym możesz przeglądać wszystkie ankiety dla danej lokalizacji.",
          path: rootUrl + "polls/"
        }, {
          element: "#tour-Followers",
          title: "Obserwatorzy",
          content: "Sprawdź kto jeszcze jest zaangażowany w rozwój swojego miasta. Znajdziesz tu wszytskich użytkowników, którzy obserwują to miejsce.",
          path: rootUrl + "followers/"
        }, {
          element: "#tour-map-icon",
          title: "Mapa",
          content: "Przejdź do mapy aby sprawdzić co się dzieje w okolicy",
          placement: "bottom",
          path: rootUrl + "followers/"
        }, {
          element: "",
          title: "Mapa",
          content: "Dzięki mapie możemsz szybko odnaleźć wszystko co sie dzieje w okolicy.",
          path: "/maps/",
          orphan: true
        }, {
          element: "",
          title: "Kraj",
          content: "Wybierz miejsce które chciałbyś zmieniać. Pamiętaj, że to ty masz wpływ na to co się dzieje w twoim otoczeniu.",
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