(function ($) {
    "use strict";
    $('.errorlist > li').addClass('alert alert-danger');
    $('.cancel-btn').on('click', function () {
        history.go(-1);
    });
    $('.navbar-avatar').tooltip({placement: 'bottom'});
    $(document).ready(function () {
        $('.bookmarks-list-toggle').one('click', function (evt) {
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
})(jQuery);