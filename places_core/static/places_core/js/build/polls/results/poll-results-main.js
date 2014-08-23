//
// Strona wyświetlania wyników ankiety => /templates/polls/poll-results.html
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    //urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        plot: 'includes/jqplot/jquery.jqplot',
        'dateAxisRenderer': 'includes/jqplot/plugins/jqplot.dateAxisRenderer',
        'canvasTextRenderer':'includes/jqplot/plugins/jqplot.canvasTextRenderer',
        'canvasAxisTickRenderer': 'includes/jqplot/plugins/jqplot.canvasAxisTickRenderer',
        'categoryAxisRenderer': 'includes/jqplot/plugins/jqplot.categoryAxisRenderer',
        'barRenderer': 'includes/jqplot/plugins/jqplot.barRenderer'
        
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
        
        plot: {
            deps: ['jquery']
        },
        
        dateAxisRenderer: { deps: ['plot'] },
        canvasTextRenderer: { deps: ['plot'] },
        canvasAxisTickRenderer: { deps: ['plot'] },
        categoryAxisRenderer: { deps: ['plot'] },
        barRenderer: { deps: ['plot'] }
    }
});

require(['jquery',
         'dateAxisRenderer',
         'canvasTextRenderer',
         'canvasAxisTickRenderer',
         'categoryAxisRenderer',
         'barRenderer',
         'ui',
         'common',
         'js/locations/follow',
         'js/inviter/userinviter'],

function ($, ui) {
    
    "use strict";
    
    var plot1 = $.jqplot('chartdiv', [window.POLLS.asets], {
            title: window.POLLS.title,
            animate: true,
            series:[{renderer:$.jqplot.BarRenderer}],
            axesDefaults: {
                tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                tickOptions: {
                    angle: -30,
                    fontSize: '10pt'
                }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer
                }
            }
        });
    
    $(document).trigger('load');
    
});