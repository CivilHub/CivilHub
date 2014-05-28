var jQ = jQuery.noConflict();
//
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
// -----------------------------------------------------------------------------
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
//
// Custom shorthand for sending AJAX requests in Django.
// -----------------------------------------------------------------------------
function sendAjaxRequest(type, url, opts) {
    var defaults = {
            data: {},
            dataType: 'json',
            success: function (resp) {
                display_alert('Changes saved', 'success');
            },
            error: function (err) {
                display_alert(err.responseJSON.detail, 'danger');
            }
        },
        options = jQ.extend(defaults, opts);
    return (function () {
        jQ.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
        jQ.ajax({
            type: type,
            url: url,
            data: options.data,
            dataType: options.dataType,
            success: options.success,
            error: options.error
        });
    })();
}