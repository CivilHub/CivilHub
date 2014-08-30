({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
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
    },
    name: "js/build/polls/results/poll-results-main",
    out: "poll-results-built.js"
})