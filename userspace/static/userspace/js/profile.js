//
// profile.js
// ==========
//
// User activities from profile page.
//
var app = app || {};

app.ActionModel = Backbone.Model.extend({
    defaults: {
        'description': ''
    }
});

app.ActionView = Backbone.View.extend({
    
    tagName: 'div',
    
    className: 'row user-action-entry',
    
    template: _.template($('#action-template').html()),
    
    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

app.ActionCollection = Backbone.Collection.extend({
    
    model: app.ActionModel,
    
    url: app.actionApiUrl
});

app.ActionList = Backbone.View.extend({
    
    el: '.user-activity-stream',
    
    initCollection: function (callback, context) {
        $.ajax({
            type: 'GET',
            url: app.actionApiUrl,
            data: {'user_id':app.actionUserId},
            success: function (resp) {
                if (typeof(callback) === 'function') {
                    callback.call(context, resp);
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    },
    
    initialize: function () {
        this.initCollection(function (actions) {
            this.collection = new app.ActionCollection(actions);
            this.render();
        }, this);
    },
    
    render: function () {
        this.collection.each(function (item) {
            this.renderItem(item);
        }, this);
    },
    
    renderItem: function (item) {
        var view = new app.ActionView({
            model: item
        });
        $(view.render().el).appendTo(this.$el);
    }
});

app.actions = new app.ActionList();
