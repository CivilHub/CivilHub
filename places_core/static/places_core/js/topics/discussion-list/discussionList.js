//
// discussionList.js
// =================
// Main view for list of discussions.
define(['jquery',
        'underscore',
        'backbone',
        'js/utils/utils',
        'js/topics/discussion-list/discussionEntry',
        'js/topics/discussion-list/discussionCollection',
        'js/ui/paginatorView'],
        
function ($, _, Backbone, utils, DiscussionEntry, DiscussionCollection, PaginatorView) {
    "use strict";
    
    var baseurl = $('#discussion-api-url').val();
    
    var DiscussionList = Backbone.View.extend({
        el: '#discussions',
        
        _init: function (data) {
            var that = this;
            this.collection = new DiscussionCollection(data.results);
            this.$el.empty();
            this.render();
            if (this.paginator !== undefined) {
                this.paginator.$el.empty().remove();
            }
            this.paginator = new PaginatorView({
                count: data.count,
                perPage: 2,
                targetCollection: this.collection
            });
            $(this.paginator.render().el).insertAfter(this.$el);
            this.listenTo(this.collection, 'sync', this.render);
        },
        
        initialize: function () {
            var self = this;
            $.get(baseurl, function (resp) {
                if (resp.count) {
                    self._init(resp);
                } else {
                    self.$el.append('<p class="alert alert-info">' + gettext("There are no discussions yet") + '</p>');
                }
            });
        },
        
        render: function () {
            this.$el.empty();
            this.collection.each(function (item) {
                this.renderItem(item);
            }, this);
        },
        
        renderItem: function (item) {
            var view = new DiscussionEntry({model:item});
            $(view.render().el).appendTo(this.$el);
        },
        
        filter: function (page) {
            var that = this,
                filters = utils.getListOptions(),
                url = baseurl + '&' + utils.JSONtoUrl(filters);
            this.collection.url = url;
            this.collection.fetch();
        }
    });
    
    return DiscussionList;
});