
// Accordion menu and article content loader for Help and Support page.

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox'
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
        
        tagsinput: {
            deps: ['jquery']
        },
    }
});

require(['jquery',
         'js/common'],
         
function ($) {
    
    "use strict";
    
    $('#category-menu a').on('click', function (e) {
        e.preventDefault();
        $('#category-menu').find('.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.category-entry > a').on('click', function (e) {
        
        e.preventDefault();
        
        var $sublist = $(this).next('.sublist');
        
        // Holds proper classname for first element to show (category/article)
        
        var current = null;
        
        $(this).parent().siblings().each(function () {
            $(this)
                .find('.sublist:first')
                .not($sublist)
                    .slideUp('fast')
                .find('.sublist')
                    .slideUp('fast');
        });
        
        // If list is empty, ignore
        if ($sublist.is(':empty')) return false;
        
        $sublist.slideToggle('fast', function () {
            
            // If there are articles, show first, otherwise expand first category.
            if ($(this).children('.article-link').length >= 1) {
                current = '.article-link:first';
            } else {
                current = '.category-entry:first'
            }
            $sublist.children(current).find('a:first').trigger('click');
        });
    });
    
    $('.article-link > a').on('click', function (e) {
        e.preventDefault();
        $.get($(this).attr('href'), function (content) {
            $('#article-content').html(content);
        });
    });
    
    $('.category-entry:first').find('a').trigger('click');
    
    $(document).trigger('load');
    
});