/*
 * location-list.js
 * ================
 * 
 * Przeglądarka lokalizacji w formie mapy wektorowej.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        vector     : "includes/vectormap/jquery-jvectormap-1.2.2.min",
        worldmap   : "includes/vectormap/jquery-jvectormap-world-mill-en",
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
        
        vector: {
            deps: ["jquery"]
        },
        
        worldmap: {
            deps: ["vector"]
        },

        tour: {
            deps: ["jquery"]
        },
    }
});

require(['jquery',
         'js/modules/locations/location-list/col-view',
         'vector',
         'worldmap',
         'js/modules/common',
         'js/modules/locations/follow',
         'tour'], 

function ($, ColView) {
    
    // openPlaceholderWindow
    // ---------------------
    // Helper function: otwiera główne okno przechowujące listy
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
    // Helper function: zamyka główne okno przechowujące listy
    // ---------------------------------------------------------------------
    var closePlaceholderWindow = function () {
        $('#list-placeholder').fadeOut('slow', function () {
            $(this).find('.placeholder-content').empty();
            delete window.activeSublist;
        });
    };
    
    // openList
    // --------
    // Właściwa funkcja, która otwiera pierwszy "poziom" listy albo wyświetla
    // alert jeżeli w bazie nie ma kraju o podanym kodzie.
    //
    // @param event { jQuery.event || vectorMap.event} przechwycony klik
    // @param code  { string } Dwuliterowy kod kraju (case insensitive)
    // ---------------------------------------------------------------------
    var openList = function (event, code) {
        // Jeżeli jest już aktywna lista dla jakiegoś kraju, nie otwieraj
        // nowego okna.
        if (window.activeSublist !== undefined && window.activeSublist) {
            return false;
        }
        // Sprawdzamy, czy kraj jest już w bazie. Jeżeli tak, otwieramy listę.
        $.get('/api-locations/countries/?code=' + code, function (resp) {
            if (resp.length) {
                // Bezwzględnie koniecznie jako pierwszy argument podajemy
                // pustą tabelę - Backbone zawsze traktuje pierwszy argument
                // jako kolekcję, co tutaj prowadzi do błędów.
                var locationList = new ColView([], resp[0].location, 1);
                window.activeSublist = locationList;
                locationList.on('destroyed', function () {
                    closePlaceholderWindow();
                });
                openPlaceholderWindow();
            } else {
                // TODO: coś tu trzeba pokazać.
                //alert("There is no such place");
                var dialog = $('#no-place-dialog');
                dialog.fadeIn();
                dialog
                    .find('.placeholder-close')
                    .on('click', function(e){
                        dialog.fadeOut();
                    });
            }
        });
    };
    
    var showPopup = function(countryCode) {
        $.get('/api-locations/locations/?code=' + countryCode, function (resp) {
            if (resp) {
                //$('#countryName').text(resp.name);
                //$('#countryName').attr('href', '/' + resp.slug);
                
                var followButton = $('#follow-button');
                var targetID = resp.id;
                var name = resp.name;
                followButton.attr('data-target', targetID);
                
                if(resp.followed) {
                    followButton
                        .addClass('btn-unfollow-location')
                        .text(gettext('You are following') + ' ' + name);
                } else {
                    followButton
                        .addClass('btn-follow-location')
                        .text(gettext('Follow') + ' ' + name);
                }
                
                followButton.on('click', function(e) {
                    e.preventDefault();
                    if( followButton.hasClass('btn-unfollow-location') ) {
                        $.post('/remove_follower/' + targetID, 
                            {csrfmiddlewaretoken: getCookie('csrftoken')}, 
                            function (resp) {
                                followButton
                                    .addClass('btn-follow-location')
                                    .removeClass('btn-unfollow-location')
                                    .text(gettext('Follow') + ' ' + name);
                        });
                    } else {
                        $.post('/add_follower/' + targetID,
                            {csrfmiddlewaretoken: getCookie('csrftoken')}, 
                            function (resp) {
                                followButton
                                    .addClass('btn-unfollow-location')
                                    .removeClass('btn-follow-location')
                                    .text(gettext('You are following') + ' ' + name);
                        });
                    }
                });
                
            } else {
                alert("There is no such place");
            }
        });
    };
    
    // Mapa
    // ----
    // Wyświetla mapę wektorową i uruchamia po kliknięciu odpowiednią listę.
    // ---------------------------------------------------------------------
    $('#vector-map').vectorMap({
        
        map: 'world_mill_en', 
        
        backgroundColor: 'transparent',
        
        onRegionClick: function(element, code, region) {
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
    // Uruchamianie listy lokalizacji po kliknięciu na nazwę państwa.
    // ---------------------------------------------------------------------
    $('.country-entry').on('click', function (e) {
        e.preventDefault();
        var countryCode = $(this).attr('data-code');
        openList(e, countryCode);
        // Sprawdzamy, czy kraj jest już w bazie. Jeżeli tak, otwieramy listę.
        showPopup(countryCode);
        
        
    });
    
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