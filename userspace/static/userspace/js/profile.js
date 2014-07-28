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
    
    filterContent: false,
    
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
        this.$spinner = $(document.createElement('span'));
        this.$spinner
            .addClass('fa fa-spin fa-circle-o-notch')
            .hide();
        this.initCollection(function (actions, next) {
            this.setPage(next);
            this.collection = new app.ActionCollection(actions);
            this.render();
            this.listenTo(this.collection, 'add', this.renderItem);
        }, this, {'user_id':app.actionUserId});
    },
    
    filter: function (content) {
        this.filterContent = content || false;
        var data = {};
        data.user_id = app.actionUserId;
        if (this.filterContent) data.content = this.filterContent;
        this.initCollection(function (actions, next) {
            this.setPage(next);
            this.collection.reset(actions);
            this.render();
        }, this, data);
    },
    
    setPage: function (next) {
        if (next) this.nextPage = next.slice(next.indexOf('&page')+6);
        else this.nextPage = null;
    },
    
    getPage: function (page) {
        page = page || this.nextPage;
        if (_.isNull(page)) return false;
        this.$spinner.appendTo(this.$el).fadeIn('fast');
        var data = {
            'user_id': app.actionUserId,
            'page': this.nextPage
        }
        if (this.filterContent) data.content = this.filterContent;
        this.initCollection(function (actions, next) {
            this.setPage(next);
            _.each(actions, function (item) {
                this.collection.add(item);
            }, this);
            this.$spinner.fadeOut('fast');
        }, this, data);
    },
    
    render: function () {
        this.$el.empty();
        this.collection.each(function (item) {
            this.renderItem(item);
        }, this);
        this.$spinner.appendTo(this.$el);
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
// Enable lazy-loading on page scrolling
$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
       app.actions.getPage();
   }
});
