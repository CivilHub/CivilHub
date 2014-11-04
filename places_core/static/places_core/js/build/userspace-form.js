({
    baseUrl: "../../",
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        jqueryui   : "includes/jquery-ui/jquery-ui",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        bootstrap  : "includes/bootstrap/bootstrap",
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
        
        jqueryui: {
            deps: ["jquery"]
        },
        
        color: {
            deps: ["jquery"]
        },
        
        Jcrop: {
            deps: ["jquery"]
        },
        
        "file-input": {
            deps: ["bootstrap"]
        }
    },
    name: "js/src/userspace-form",
    out: "../dist/userspace-form.js"
})