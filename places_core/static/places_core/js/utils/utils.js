//
// utils.js
// ========
//
// Collection of simple tools to deal with
// Django REST framework.
//
define(['jquery'], function ($) {
    "use strict";
    
    var utils = utils || {};

    //
    // Csrf protection methods.
    // see: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    // -----------------------------------------------------------------------------
    utils.csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };
    utils.sameOrigin = function (url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    };
    //
    // Get cookie by name
    // ------------------
    // @param {string} name Cookie's name
    // @returns {string} Cookie's value
    utils.getCookie = function (name) {
        "use strict";
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    
    //
    // Funkcja konwertuje zapytanie GET na JSON.
    // -----------------------------------------
    // @returns Obj
    utils.urlToJSON = function (url) {
        var urlItems = [],
            jsonData = {},
            i, itm;
            
        url = url.split('?')[1] || false;
        
        if (!url) {
            return {}; // Brak danych GET.
        }
        
        url = url.split('&');
        
        for (i = 0; i < url.length; i++) {
            itm = url[i].split('=');
            jsonData[itm[0]] = itm[1];
        }
        
        return jsonData;
    }
    //
    // Funkcja serializuje proste obiekty do URL.
    // ------------------------------------------
    // @param {JSON Obj} json Obiekt do konwersji
    utils.JSONtoUrl = function (json) {
        var pairs = _.pairs(json),
            urlitems = [],
            i;
        
        for (i = 0; i < pairs.length; i++) {
            urlitems.push(pairs[i].join('='));
        }
        
        return urlitems.join('&');
    }
    
    //
    // Helper functions
    // ================
    // Funkcja pobierająca dodatkowe dane z formularza 'search'.
    // ---------------------------------------------------------
    utils.getSearchText = function () {
        var $field = $('#haystack'),
            txt = $field.val();
        
        if (_.isUndefined(txt) || txt.length <= 1) {
            return '';
        }
        
        return txt;
    };
    //
    // Wczytanie wybranych opcji.
    // ---------------------------
    // Sprawdzenie aktywnych elementów (klikniętych linków)
    // w celu "pozbierania" opcji wyszukiwarki.
    // 
    utils.getListOptions = function () {
        var $sel = $('.list-controller'),
            opts = {},
            optType = null,
            optValue = null;
        
        $sel.each(function () {
            var $this = $(this);
            
            if ($this.hasClass('active')) {
                optType = $this.attr('data-control');
                optValue = $this.attr('data-target');
                opts[optType] = optValue;
            }
        });
        
        opts['haystack'] = utils.getSearchText();
        
        return opts;
    };
    
    return utils;
});