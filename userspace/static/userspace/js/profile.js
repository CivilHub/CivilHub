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
    
    nextPage: null,
    
    initCollection: function (callback, context, data) {
        $.ajax({
            type: 'GET',
            url: app.actionApiUrl,
            data:  data || {},
            success: function (resp) {
                if (typeof(callback) === 'function') {
                    callback.call(context, resp.results, resp.next);
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    },
    
    initialize: function () {
        this.initCollection(function (actions, next) {
            this.nextPage = next || null;
            this.collection = new app.ActionCollection(actions);
            this.render();
        }, this, {'user_id':app.actionUserId});
    },
    
    filter: function (content) {
        content = content || false;
        var data = {};
        data.user_id = app.actionUserId;
        if (content) data.content = content;
        this.initCollection(function (actions, next) {
            this.nextPage = next || null;
            this.collection.reset(actions);
            this.render();
        }, this, data);
    },
    
    render: function () {
        this.$el.empty();
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
// Check if there is a better way to handle external events.
$('.list-controller').on('click', function (e) {
    e.preventDefault();
    app.actions.filter($(this).attr('data-target'));
});
