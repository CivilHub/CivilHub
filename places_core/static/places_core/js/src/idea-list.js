/*
 * idea-list.js
 * ============
 * 
 * Strona listy pomysłów w pojedynczej lokalizacji.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        bootstrap  : "includes/bootstrap/bootstrap",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        paginator  : "includes/backbone/backbone.paginator",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootbox    : "includes/bootstrap/bootbox",
        moment     : "includes/momentjs/moment",
        tour       : "includes/tour/bootstrap-tour"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        underscore: {
            deps: ["jquery"],
            exports: "_"
        },
        
        backbone: {
            deps: ["underscore"],
            exports: "Backbone"
        },
        
        bootstrap: {
            deps: ["jquery"]
        },
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        },
        
        tagsinput: {
            deps: ["jquery"]
        },

        tour: {
            deps: ["jquery"]
        }
    }
});

require(['jquery',
         'js/modules/common',
         'js/modules/locations/follow',
         'js/modules/ideas/idea-list/ideas',
         'js/modules/ideas/votes/votes',
         'js/modules/ideas/category-creator',
         'js/modules/inviter/userinviter',
         'tour'],

function ($) {
    
    "use strict";
    
    //tour start button
    $('.main-page-content').append('<div class="tourBox"><a href="#" class="btn btn-saveBig" id="startTour"><span class="fa fa-play">Start Tour</span></a></div>');
    //Instance the tour
     var tour = new Tour({
        steps: [{
            element: "#tour-location-name",
            title: "Jesteś tutaj",
            content: "Widzisz właśnie nazwę lokalizacji, w której aktualnie się znajdujesz.",
            path: "/warsaw-pl/"
        }, {
            element: "#tour-Summary",
            title: "Podsumowanie",
            content: "W tym miejscu możesz obserwować wszystkie aktywności dla tej lokalizacji.",
            path: "/warsaw-pl/"
        }, {
            element: "#tour-summary-box",
            title: "Aktywność",
            content: "Aktywności przedstawiamy tobie w taki oto sposób. Każda aktywność posiada własną kategorię (m.in. Ankieta, Dyskusja, Pomysł itp). Możesz do nich przechodzić bezpośrednio klikając w treść znajdującą się pod tytułem.",
            backdrop: true,
            path: "/warsaw-pl/"
        }, {
            element: "#tour-activity",
            title: "Aktywność użytkowników",
            content: "W tym miejscu znajdują się wszytskie aktywności jakie dany użytkownik wykonał dla tego miejsca.",
            backdrop: true,
            path: "/warsaw-pl/"
        }, {
            element: "#tour-Blog",
            title: "Blog",
            content: "Znajdziesz tutaj wszystkie aktualności związane z tą lokalizacją. Ponadto możesz tworzyć własne aktualności wybierając w panelu bocznym dodaj aktualność. ",
            path: "/warsaw-pl/news/"
        }, {
            element: "#tour-Discussions",
            title: "Dyskusje",
            content: "Możesz przglądać dyskusje poruszone w tej lokalizacji bądź samemy dołączyć do takiej dyskusji. Tworzenie nowych dyskusji jest również w twojej mocy.",
            path: "/warsaw-pl/discussion/"
        }, {
            element: "#tour-Ideas",
            title: "Pomysły",
            content: "Przeglądaj pomysły użytkowników i oceniaj je. Dziel się również swoimy ciekawymi pomysłami.",
            path: "/warsaw-pl/ideas/"
        }, {
            element: "#tour-votes",
            title: "Głosowanie",
            content: "Tu oddajesz swój głos. Możesz przeglądać głosy innych klikająć w ilość głosów w dolnej części okienka.",
            backdrop: true,
            path: "/warsaw-pl/ideas/"          
        }, {
            element: "#tour-Polls",
            title: "Ankiety",
            content: "Miejsce, w którym możesz przeglądać wszystkie ankiety dla danej lokalizacji.",
            path: "/warsaw-pl/polls/"
        }, {
            element: "#tour-Followers",
            title: "Obserwatorzy",
            content: "Sprawdź kto jeszcze jest zaangażowany w rozwój swojego miasta. Znajdziesz tu wszytskich użytkowników, którzy obserwują to miejsce.",
            path: "/warsaw-pl/followers/"
        }, {
            element: "#tour-map-icon",
            title: "Mapa",
            content: "Przejdź do mapy aby sprawdzić co się dzieje w okolicy",
            placement: "bottom",
            path: "/warsaw-pl/followers/"
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
    //rozpoczynam tour od kroku 1 
    $("#startTour").click(function (e){
        e.preventDefault();
        tour.restart();
        tour.start();
    });

    $(document).trigger('load');
    
});