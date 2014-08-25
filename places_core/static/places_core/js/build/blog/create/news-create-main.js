//
// Formularz tworzenia nowego wpisu na blog.
//  => /templates/locations/location_news_form.html
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        ckeditor: 'includes/ckeditor/ckeditor',
        dropzone: 'includes/dropzone/dropzone',
        jqueryui: 'includes/jquery-ui/jquery-ui'
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
        
        ckeditor: {
            exports: 'CKEDITOR'
        },
        
        dropzone: {
            exports: 'Dropzone'
        },
        
        jqueryui: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/locations/newsForm',
         'ui',
         'common',
         'js/locations/follow',
         'js/blog/category-creator'],

function ($, NewsForm) {
    
    var form = new NewsForm();
    
    $(document).trigger('load');
    
});