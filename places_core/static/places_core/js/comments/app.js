var app = app || {}
var $ = jQuery.noConflict();
$(document).ready(function ($) {
    $(document).on('click', '.comment-toggle', function (evt) {
        var $handle = $(this),
            targetId = $handle.attr('data-target'),
            url = '/comments/tree/' + targetId + '/blog/News';
           
        $.get(url, function (resp) {
            resp = JSON.parse(resp);
            console.log(resp);
            comment_tree = new app.CommentListView(resp);
        });
    });
});