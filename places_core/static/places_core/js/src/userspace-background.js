/*
 * userspace-background.js
 * =======================
 * 
 * Zmiana obrazu tła dla profilu użytkownika.
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
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootbox    : "includes/bootstrap/bootbox",
        color      : "includes/jquery/jquery.color",
        Jcrop      : "includes/jquery/jquery.Jcrop",
        "file-input": "includes/bootstrap/bootstrap.file-input"
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
        
        color: {
            deps: ["jquery"]
        },
        
        Jcrop: {
            deps: ["color"]
        },
        
        "file-input": {
            deps: ["bootstrap"]
        }
    }
});

require(['jquery',
         'js/modules/ui/image-form',
         'js/modules/common'],

function($, ImageForm) {
    
    "use strict";
    
    $(document).ready(function () {
        var form = new ImageForm({
            $el: $('#user-background-form'),
            orientation: 'landscape'
        });
    });
    
    $(document).trigger('load');
    
});