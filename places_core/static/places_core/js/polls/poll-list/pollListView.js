//
// pollListView.js
// ===============
// Generic poll list view for selected location.
define(['jquery',
        'underscore',
        'backbone',
        'js/utils/utils',
        'js/polls/poll-list/pollListEntry',
        'js/polls/poll-list/pollListCollection'],

function ($, _, Backbone, utils, PollListEntry, PollListCollection) {
    
    "use strict";
    
    var baseurl = $('#poll-api-url').val();
    
    var PollListView = Backbone.View.extend({
        el: '#polls',
            
        _init: function (data) {
            var that = this;
            this.collection = new PollListCollection(data.results);
            this.$el.empty();
            this.render();
        },
        
        initialize: function () {
            var that = this;
            $.get(baseurl, function (resp) {
                that._init(resp);
            });
        },
        
        render: function () {
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
                url  = baseurl + '&' + utils.JSONtoUrl(filters);
            if (page) url += '&page=' + page;
            $.get(url, function (resp) {
                that._init(resp);
            });
        }
    });
    
    return PollListView;
});