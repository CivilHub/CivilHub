//
// Formularz do tworzenia nowych lokalizacji.
//
//  => /templates/location/location_form.html
//
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        'bootstrap-fileinput': 'includes/bootstrap/bootstrap.file-input',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        mapinput: 'js/ui/jquery.mapinput',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common'
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
        
        mapinput: {
            deps: ['jquery']
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        'bootstrap-fileinput': {
            deps: ['bootstrap']
        },
    }
});

require(['jquery',
         'js/locations/location-form',
         'common',],

function ($, LocationForm) {
    
    "use strict";
    
    //~ $(document).ready(function () {
        //~ var form = new LocationForm();
    //~ });
    
    $(document).trigger('load');
    
});