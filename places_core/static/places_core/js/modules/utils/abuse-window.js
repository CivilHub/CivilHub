//
// abuse-report.js
// ===============
//
// Allow registered users to send abuse reports related to content.
//
// By creating a window we pass to the constructor an object with basic
// parameters that become our 'default' values. The object should contain:
//
//   - id      => object id that we mark as object_pk)
//   - content => id for the content type (ContentType) of the marked object
//
// TODO: It is worthwhile to think about cathing errors from the server.
//

define(['jquery',
        'underscore',
        'js/modules/ui/ui',
        'js/modules/utils/utils',
        'bootstrap'],

function ($, _, ui, utils) {

    "use strict";
    
    var AbuseWindow = function (targetData) {
        this.data = targetData || {'id': 0, 'content': 0};
        this.template = _.template($('#abuse-modal-tpl').html());
        this.$el = $(document.createElement('div'));
        this.$el
            .addClass('modal fade')
            .html(this.template(this.data))
            .modal({'show':false});

        this.$form = this.$el.find('form:first');

        this.$el.find('.submit-btn').on('click', function (e) {
            e.preventDefault();
            this.$form.trigger('submit');
        }.bind(this));

        this.$form.on('submit', function (e) {
            e.preventDefault();
            this.submit();
        }.bind(this));
    };
    
    AbuseWindow.prototype.open = function () {
        this.$el.modal('show');
    };
    
    AbuseWindow.prototype.close = function () {
        this.$el.modal('hide');
    };
    
    AbuseWindow.prototype.submit = function () {
        var data = this.$form.serializeArray();
        $.ajaxSetup({
            headers: {'X-CSRFToken': utils.getCookie('csrftoken')}
        });
        $.post('/rest/reports/', data, function () {
            this.close();
            ui.message.success(gettext("Report sent"));
        }.bind(this));
    };
    
    return AbuseWindow;
});