//
// content-collection.js
// =====================

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/actstream/actions/actionCollection',
        'js/modules/locations/contents/content-view',
        'jpaginate'],

function ($, _, Backbone, ActionCollection, ActionView) {
    
  "use strict";
  
  var apiUrl  = window.CONTENT_API_URL;
  
  var apiUser = window.LOCATION_ID;
  
  var ActionList = Backbone.View.extend({
  
    el: '#location-content-collection',
    
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
      }, this, {'pk':apiUser});
    },
    
    filter: function (options) {
      var data = options || {};
      data.pk = apiUser;
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
        'pk': apiUser,
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
        this.$el.append('<div class="row"></div>')
        if (this.collection.length > 0) {
          this.collection.each(function (item) {
            this.renderItem(item);
          }, this);
          this.$spinner.appendTo(this.$el);
          $('.col-sm-9.colHline').addClass('colHlineR');
          $('.col-sm-3.colHline').addClass('colHlineL');
        } else {
          this.$el.append('<p class="alert alert-info">' + gettext("No activity yet") + '</p>');
        }
    },
    
    renderItem: function (item) {
      var view = new ActionView({model: item});
      $(view.render().el)
        .appendTo(this.$el.find('.row:last'))
        .find('.locBoxHeader:first')
        .css('background', "url(" + item.get('thumbnail') + ") left top no-repeat");
      if (this.$el.find('.row:last').find('.locBoxH').length >= 4) {
        this.$el.append('<div class="row"></div>');
      }
    }
  });
  
  return ActionList;
  
});