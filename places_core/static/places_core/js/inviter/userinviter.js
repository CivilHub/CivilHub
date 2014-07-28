//
// userinviter.js
// ==============
// Allow registered user to invite others fro browsing content.
require(['jquery', 'tagsinput', 'bootstrap'],

function ($) {
    
    "use strict";
    
    var $modal     = $('#invite-modal'),               // Modal window
        $toggle    = $('#invite-people-toggle'),       // Toggle link (open modal)
        $form      = $modal.find('form:first'),        // Form
        $submit    = $modal.find('.submit-btn'),       // Submit button
        $emails    = $('#invite-emails'),              // Emails input
        inviteText = $emails.attr('data-defaulttext'), // Text for TagsInput
        apiUrl     = $form.attr('action'),             // Api target URL
        currentUrl = window.location.href;             // Current page address

    $modal.modal({show:false});

    $emails.tagsInput({
        defaultText: inviteText,
        onPaste: true,
        onAddTag: function () {
            var oldValue = $emails.val(),
                newValue = oldValue.replace(/ /g, ',');
            $emails.importTags('');
            $emails.importTags(newValue);
        }
    });

    $form.on('submit', function (evt) {
        evt.preventDefault();
    });

    $toggle.bind('click', function (evt) {
        evt.preventDefault();
        $modal.modal('show');
    });

    $submit.bind('click', function (evt) {
        evt.preventDefault();
        $modal.modal('hide');
        sendAjaxRequest('POST', apiUrl, {
            data: {
                'emails': $emails.val(),
                'link': currentUrl,
                'name': document.title
            },
            success: function (resp) {
                display_alert(resp.message, resp.level);
            }
        });
    });
});