(function ($) {
    "use strict";
    $('.errorlist > li').addClass('alert alert-danger');
    $('.cancel-btn').on('click', function () {
        history.go(-1);
    });
    $('.navbar-avatar').tooltip({placement: 'bottom'});
    //~ $('.report-abuse-link').bind('click', function (evt) {
        //~ var target = evt.currentTarget,
            //~ targetUrl = $(target).attr('href'),
            //~ params = targetUrl.split('/'),
            //~ appLabel = params[2],
            //~ modelLabel = params[3],
            //~ objectPk = params[4];
        //~ evt.preventDefault();
        //~ console.log(evt.currentTarget);
        //~ console.log(params);
        //~ sendAjaxRequest('POST', '/rest/reports/', {
            //~ data: {
                //~ comment: 'Test via AJAX',
                //~ object_pk: objectPk,
                //~ content_type: modelLabel
            //~ },
            //~ success: function(resp) {
                //~ console.log(resp);
            //~ },
            //~ error: function (err) {
                //~ console.log(err.responseJSON);
            //~ }
        //~ });
    //~ });
})(jQuery);