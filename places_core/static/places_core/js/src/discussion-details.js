/*
 * discussion-details.js
 * =====================
 * 
 * Detailed view of single forum discussion.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        paginator  : "includes/backbone/backbone.paginator",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        leaflet    : "includes/leaflet/leaflet",
        "tour": "includes/tour/bootstrap-tour"
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

        "tour": {
            "deps": ["bootstrap"]
        },
        
        jqueryui: {
            deps: ["jquery"]
        },
        
        tagsinput: {
            deps: ["jquery"]
        }
    }
});

require(['jquery',
         'js/modules/ui/ui',
         'js/modules/maps/pointer',
         'js/modules/ui/mapinput',
         'js/modules/common',
         'js/modules/ui/bookmark-form',
         'js/modules/locations/follow',
         'js/modules/inviter/userinviter',
         'js/modules/topics/reply-form',
         'js/modules/topics/category-creator'],

function ($, ui, Minimap) {
    
    "use strict";
    
    //
    // Save user's vote on server
    // --------------------------
    // @param {boolean} vote
    // @param {string} url
    // @param {jQuery Object} $counter
    //
    var sendVote = function (vote, url, $counter) {
        var votes = parseInt($counter.text(), 10) || 0;
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                vote: vote,
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]:first').val()
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success) {
                    message.success(resp.message);
                    $counter.text(++votes);
                } else {
                    message.warning(resp.message);
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    };
    
    $('.entry-vote-up').on('click', function (e) {
        e.preventDefault();
        var vote = true;
        var url = $(this).attr('href');
        var $counter = $(this).siblings('.entry-vote-count');
        sendVote(vote, url, $counter);
    });
    
    $('.entry-vote-down').on('click', function (e) {
        e.preventDefault();
        var vote = false;
        var url = $(this).attr('href');
        var $counter = $(this).siblings('.entry-vote-count');
        console.log($counter);
        sendVote(vote, url, $counter);
    });
    
    $(document).trigger('load');
    
});