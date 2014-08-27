({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap'
    },
    
    shim: {
        bootstrap: {
            deps: ['jquery']
        },
    },
    name: "js/build/userspace/login/userspace-login-main",
    out: "userspace-login-built.js"
})