//
// actionList.js
// =============
//
// Entire action list view.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/userspace/actions/actionCollection',
        'js/userspace/actions/actionView'],

function ($, _, Backbone, ActionCollection, ActionView) {
    "use strict";
    
    var apiUrl = $('#rest-api-url').val();
    
    var apiUser = $('#rest-api-usr').val();
    
    var ActionList = Backbone.View.extend({
    
        el: '.activity-stream',
        
        nextPage: null,
        
        filterContent: false,
        
        initCollection: function (callback, context, data) {
            $.ajax({
                type: 'GET',
                url: apiUrl,
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
                this.collection = new ActionCollection(actions);
                this.render();
                this.listenTo(this.collection, 'add', this.renderItem);
            }, this, {'user_id':apiUser});
        },
        
        filter: function (content) {
            this.filterContent = content || false;
            var data = {};
            data.user_id = apiUser;
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
                'user_id': apiUser,
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
            if (this.collection.length > 0) {
                this.collection.each(function (item) {
                    this.renderItem(item);
                }, this);
                this.$spinner.appendTo(this.$el);
            } else {
                this.$el.append('<p class="alert alert-info">' + gettext("No activity yet") + '</p>');
            }
        },
        
        renderItem: function (item) {
            var view = new ActionView({
                model: item
            });
            $(view.render().el).appendTo(this.$el);
        }
    });
    
    return ActionList;
});