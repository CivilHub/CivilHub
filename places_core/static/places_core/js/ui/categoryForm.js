//
// categoryForm.js
// ===============
// Create new category for different modules using modal form. This class's
// main purpose is to be extended with url parameters pointing to REST api
// for selected module's categories.
define(['jquery',
        'underscore',
        'backbone',
        'js/utils/utils',
        'js/ui/ui',
        'bootstrap'],

function ($, _, Backbone, utils, ui) {
    "use strict";
    
    var CategoryForm = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'modal fade',
        
        template: _.template($('#new-category-form').html()),
        
        events: {
            'click .submit-btn': 'submit'
        },
        
        initialize: function () {
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!utils.csrfSafeMethod(settings.type) && 
                        utils.sameOrigin(settings.url)) {
                            
                        xhr.setRequestHeader("X-CSRFToken", 
                            utils.getCookie('csrftoken'));
                    }
                }
            });
            $(this.render().el).appendTo('body');
            this.$el.modal({show:false});
            this.$form = this.$el.find('form:first');
        },
        
        render: function () {
            this.$el.html(this.template({}));
            return this;
        },
        
        open: function () {
            this.$el.modal('show');
        },
        
        close: function () {
            this.$el.modal('hide');
        },
        
        sendData: function (data, context, callback) {
            $.ajax({
                type: 'POST',
                url: context.baseurl,
                data: data,
                success: function (resp) {
                    context.close();
                    ui.message.success(gettext("New category created"));
                    if (typeof(callback) === 'function') {
                        callback.apply(context, resp);
                    }
                },
                error: function (err) {
                    if (typeof(err.responseText) !== 'undefined') {
                        context.showErrors(err.responseText);
                    }
                }
            });
        },
        
        submit: function () {
            
            var formData = {
                'name': this.$form.find('#category-name').val(),
                'description': this.$form.find('#category-description').val()
            }
            
            this.sendData(formData, this);
        },
        
        showErrors: function (errors) {
            // TODO: remember to implement this function.
            // It should display errors in form window in 
            // bootstrap alert format.
            console.log(errors);
        }
    });
    
    return CategoryForm;
});