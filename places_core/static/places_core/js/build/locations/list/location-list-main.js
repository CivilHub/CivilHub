//
//
//

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        vector: 'includes/vectormap/jquery-jvectormap-1.2.2.min',
        worldmap: 'includes/vectormap/jquery-jvectormap-world-mill-en'
    },
    
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore'],
            exports: 'Backbone'
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        vector: {
            deps: ['jquery']
        },
        
        worldmap: {
            deps: ['vector']
        }
    }
});

require(['jquery',
         'js/locations/location-list/col-view',
         'vector',
         'worldmap',
         'js/common',
         'js/locations/follow'], 

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
        $.get('/api-geo/countries/?code=' + code, function (resp) {
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
    
    $(document).trigger('load');
    
});