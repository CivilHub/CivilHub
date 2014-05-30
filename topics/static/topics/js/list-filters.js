(function ($) {
    "use strict";
    function getListOptions () {
        var $sel = $('.forum-list-control'),
            opts = {},
            optType = null,
            optValue = null;
        
        $sel.each(function () {
            var $this = $(this);
            
            if ($this.hasClass('active')) {
                optType = $this.attr('data-control');
                optValue = $this.attr('data-target');
                opts[optType] = optValue;
            }
        });
        
        return opts;
    }
    
    $('.forum-list-control').bind('click', function (evt) {
        var selectedItem = $(this).attr('data-control');
        evt.preventDefault();
        $('.active[data-control="' + selectedItem + '"]')
            .removeClass('active');
        $(this).addClass('active');
        console.log(getListOptions());
    });
})(jQuery);