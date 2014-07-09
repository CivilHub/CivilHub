//
// profile.js
// ==========
//
// User activities from profile page.
//
var app = app || {};

app.ActionModel = Backbone.Model.extend({});

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
    
    model: this.Model
});

app.ActionList = Backbone.View.extend({
    
});

app.actions = new app.ActionList();
