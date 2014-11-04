//
// votes.js
// ========
// App to manage idea votes - vote up/down.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/ui/ui'],

function ($, _, utils, ui) {
    
    "use strict";
    
    $(document).delegate('.vote-btn', 'click', function () {
        
        var formData = {
                csrfmiddlewaretoken: utils.getCookie('csrftoken'),
                idea: $(this).attr('data-target-id'),
                vote: $(this).attr('data-vote')
            },

            $votes = $(this).parents('.idea-votes:first')
                .find('.votes:first'),

            $counter = $(this).parents('.idea-votes:first')
                .find('.idea-vote-count:first'),

            votes = parseInt($counter.text(), 10) || 0,

            callback = function (data) {
                data = JSON.parse(data);
                if (data.success === true) {
                    ui.message.success(data.message);
                    $votes.html(data.votes);
                    if (!_.isNaN(votes)) {
                        $counter.text(++votes);
                    } else {
                        $counter.text(0);
                    }
                } else {
                    ui.message.warning(data.message);
                }
            };

        $.ajax({
            type: 'POST',
            url: '/ideas/vote/',
            data: formData,
            success: callback
        });
    });
});