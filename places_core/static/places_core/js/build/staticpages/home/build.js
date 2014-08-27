({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap'
    },
    
    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    },
    name: "js/build/staticpages/home/home-main",
    out: "home-built.js"
})