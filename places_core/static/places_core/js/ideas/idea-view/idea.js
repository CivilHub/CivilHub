//
// idea.js
// =======
// Scripts for detailed idea view page.
define(['ui/ui',
        'ideas/votes/counterWindow',
        'maps/pointerModal',
        'ui/bookmark-form',
        'ideas/votes/votes'],

function (ui, CounterWindow, PointerModal) {
    "use strict";
    
    $('#generic-bookmark-form').bookmarkForm({
        onSubmit: function (created) {
            if (created) {
                ui.message.success(gettext("Bookmark created"));
            } else {
                ui.message.warning(gettext("Bookmark deleted"));
            }
        }
    }).removeAttr('id');
    
    $('.idea-vote-count').on('click', function (e) {
        
        e.preventDefault();
        
        var target = $(this).attr('data-target'),
        
            CW = CounterWindow.extend({
                'ideaId': target
            }),
            
            cc = new CW();
    });
});