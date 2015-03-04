//
// support.js
// ==========
// 
// Support section pages, along with scripts to handle category menu.

require([window.STATIC_URL + "/js/config.js"], function () {
    require(['jquery',
             'js/modules/common'],
             
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
});