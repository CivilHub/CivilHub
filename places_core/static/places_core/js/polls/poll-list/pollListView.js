//
// pollListView.js
// ===============
// Generic poll list view for selected location.
define(['jquery',
        'underscore',
        'backbone',
        'js/utils/utils',
        'js/polls/poll-list/pollListEntry',
        'js/polls/poll-list/pollListCollection',
        'js/ui/paginatorView'],

function ($, _, Backbone, utils, PollListEntry, PollListCollection, PaginatorView) {
    
    "use strict";
    
    var baseurl = $('#poll-api-url').val();
    
    var PollListView = Backbone.View.extend({
        el: '#polls',
            
        _init: function (data) {
            var that = this;
            this.collection = new PollListCollection(data.results);
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
            var that = this;
            $.get(baseurl, function (resp) {
                that._init(resp);
            });
        },
        
        render: function () {
            this.$el.empty();
            this.collection.each(function (item) {
                this.renderItem(item);
            }, this);
        },
        
        renderItem: function (item) {
            var view = new PollListEntry({model:item});
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
    
    return PollListView;
});