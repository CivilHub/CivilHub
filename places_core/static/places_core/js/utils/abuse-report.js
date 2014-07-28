//
// abuse-report.js
// ===============
// Allow registered users to send abuse reports related to content.
define(['jquery',
        'underscore',
        'backbone',
        'bootstrap'],

function ($, _, Backbone) {
    "use strict";
    
    var AbuseModel = Backbone.Model.extend({
        defaults: {
            comment: "",
            content_type: 0,
            content_label: "",
            object_pk: 0,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }
    });
    
    var AbuseWindow = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'modal fade',
        
        template: _.template($('#abuse-window-tpl').html()),
        
        events: {
            'click .submit-btn': 'sendReport'
        },
        
        initialize: function (data) {
            this.model = new AbuseModel(data);
            this.render();
            this.$el.modal({show:false});
        },
        
        render: function () {
            var self = this;
            this.$el.html(this.template(this.model.toJSON()));
            this.$form = this.$el.find('form:first');
            this.$el.on('hidden.bs.modal', function () {
                self.destroy();
            });
        },
        
        open: function () {
            this.$el.modal('show');
        },
        
        close: function () {
            this.$el.modal('hide');
        },
        
        destroy: function () {
            this.$el.empty().remove();
        },
        
        sendReport: function () {
            $.ajax({
                type: 'POST',
                url: '/rest/reports/',
                data: this.$form.serializeArray(),
                success: function (resp) {
                    console.log(resp);
                    message.success(gettext("Report sent"));
                },
                error: function (err) {
                    console.log(err);
                    message.alert(gettext("An error occured"));
                }
            });
            this.close();
        }
    });
});