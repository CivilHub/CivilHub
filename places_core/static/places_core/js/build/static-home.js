({
    baseUrl: "../../",
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        tubular    : "includes/tubular/jquery.tubular.1.0"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        bootstrap: {
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
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        },
        tubular: {
            deps: ["jquery"]
        }
    },
    name: "js/src/static-home",
    out: "../dist/static-home.js"
})