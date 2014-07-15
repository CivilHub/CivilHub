//
// discussionList.js
// =================
// Main view for list of discussions.
define(['jquery',
        'underscore',
        'backbone',
        'js/utils/utils',
        'js/topics/discussion-list/discussionEntry',
        'js/topics/discussion-list/discussionCollection'],
        
function ($, _, Backbone, utils, DiscussionEntry, DiscussionCollection) {
    "use strict";
    
    var baseurl = $('#discussion-api-url').val();
    
    var DiscussionList = Backbone.View.extend({
        el: '#discussions',
        
        _init: function (data) {
            var that = this;
            this.collection = new DiscussionCollection(data.results);
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
            var view = new DiscussionEntry({model:item});
            $(view.render().el).appendTo(this.$el);
        },
        
        filter: function (page) {
            var that = this,
                filters = utils.getListOptions(),
                url = baseurl + '&' + utils.JSONtoUrl(filters);
            if (page) url += '&page=' + page;
            $.get(url, function (resp) {
                that._init(resp);
            });
        }
    });
    
    return DiscussionList;
});