(function ($) {
"use strict";
//
// Common simple scripts.
// ----------------------
// Errorlist custom styles.
$('.errorlist > li').addClass('alert alert-danger');
// Cancel button for some forms which allow back one page.
$('.cancel-btn').on('click', function () {
    history.go(-1);
});
// Tooltips for elements shared among templates.
$('.navbar-avatar').tooltip({placement: 'bottom'});
// List of user's bookmarks to fetch.
$(document).ready(function () {
    $('.bookmarks-list-toggle').one('click', function (evt) {
        console.log(evt);
        $.get('/user/my_bookmarks', function (resp) {
            var $list = $('.bookmarks-list');
            resp = JSON.parse(resp);
            if (resp.success) {
                $(resp.bookmarks).each(function () {
                    var $el = $('<li><a></a></li>'),
                        href = this.target,
                        label = this.label;
                    $el.appendTo($list).find('a')
                        .attr('href', href)
                        .text(label);
                });
            }
        });
    });
});
//
// Submenus for content entries.
// -----------------------------
$('.submenu-toggle').bind('click', function (evt) {
    var $toggle     = $(this),
        $entryTitle = $toggle.parent(),
        $submenu    = $entryTitle.next('.entry-submenu');

    if ($submenu.attr('data-opened') === undefined) {
        $submenu
            .slideDown('fast')
            .attr('data-opened', true)
            .offset({
                left: $toggle.offset().left - $(this).width(),
                top:  $toggle.offset().top + $toggle.height()
            });
    } else {
        $submenu
            .slideUp('fast')
            .removeAttr('data-opened');
    }
});

})(jQuery);