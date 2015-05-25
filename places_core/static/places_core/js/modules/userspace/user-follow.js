/**
 * user-follow.js
 * ==============
 * 
 * A script that manages the follow user button
 */

define(['jquery', 'js/modules/ui/ui'],

function ($, ui) {
    
    "use strict";
    
    function followUser (id) {
        var type = 'POST',
            url  = '/api-userspace/follow/',
            data = {pk: id},
            getCookie = window.getCookie || _getCookie,
            token = getCookie('csrftoken');

        var onSuccess = function onSuccess (response) {
            var msg = response.follow
                      ? gettext("You are following")
                      : gettext("You are not following");
            var txt = response.follow
                      ? gettext("Following")
                      : gettext("Follow");
            $('.btn-follow-user').text(txt);
            ui.message.success(msg);
        };
        
        var onError = function onError (err) {
            console.log(err);
        };

        $.ajaxSetup({
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        });
        
        $.ajax({
            type   : type,
            url    : url,
            data   : data,
            success: onSuccess,
            error  : onError
        });
    }
    
    function _getCookie (name) {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; ++i) {
            var itm = cookies[i].split('=');
            if (itm[0].trim() === name) {
                return itm[1].trim();
            }
        }
        return "";
    }
    
    $(document).ready(function () {
        $('.btn-follow-user').on('click', function (e) {
            if ($(this).attr('data-target') === undefined) {
                return true;
            }
            e.preventDefault();
            followUser($(this).attr('data-target'));
        });
    });
    
    return true;

});