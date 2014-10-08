//
// Widok pojedynczej dyskusji
//
//  => /templates/topics/discussion_detail.html
//
// --------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
        tagsinput: 'includes/jquery/jquery.tagsinput'
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
        
        jqueryui: {
            deps: ['jquery']
        },
        
        tagsinput: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/ui/ui',
         'js/maps/pointer',
         'js/ui/mapinput',
         'js/common',
         'js/ui/bookmark-form',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/topics/reply-form',
         'js/topics/category-creator'],

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