({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        validate: 'js/ui/validate'
    },
    
    shim: {
        validate: {
            deps: ['jquery']
        },
        
        bootstrap: {
            deps: ['jquery']
        }
    },
    name: "js/build/staticpages/home/home-main",
    out: "home-built.js"
})