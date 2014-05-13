(function ($) {
    "use strict";
    $('.errorlist > li').addClass('alert alert-danger');
    $('.cancel-btn').on('click', function () {
        history.go(-1);
    });
    //~ $('.report-abuse-link').on('click', function (evt) {
        //~ evt.preventDefault();
        //~ console.log(evt.currentTarget);
    //~ });
})(jQuery);