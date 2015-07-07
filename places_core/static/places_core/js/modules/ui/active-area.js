//
// active-area.js
// ==============

// Press @ to get userlist.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/caret-position',
        'text!tpl/active-area/result.html'],

function ($, _, Backbone, getCaretCoordinates, resultHTML) {

"use strict";

var ResultCollection = Backbone.Collection.extend({
  url: '/api-userspace/mention/'
});

var ResultView = Backbone.View.extend({

  tagName: 'li',

  template: _.template(resultHTML),

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    this.$el.attr('data-resultId', this.model.get('id'));
    this.$el.on('click', function (e) {
      this.trigger('activate', this.model);
    }.bind(this));
    return this;
  },

  show: function () {
    this.$el.show();
  },

  hide: function () {
    this.$el.hide();
  }
});

var ActiveArea = Backbone.View.extend({

  _active: false,

  _initialized: false,

  initialize: function (options) {
    this.$el.parent().addClass('active-area-placeholder');
    this.$list = $('<ul class="active-area-popup"></ul>');
    this.$list.insertAfter(this.$el);
    this.$el.on('keyup', function (e) {
      this.checkInput(e.keyCode);
    }.bind(this));
    this.collection = new ResultCollection();
    this.listenTo(this.collection, 'sync', this.displayResults);
    this.listenTo(this.collection, 'add', this.displayResult);
    this.replaceContent();
  },

  // FIXME: find some more efficient way to replace mention links.

  replaceContent: function () {
    var re = new RegExp(/\@<a(.*?([\w-]+))<\/a>/g);
    var value = this.$el.val() || "";
    var res = value.match(re);
    var username = "";
    _.each(res, function (match) {
      username = $(match.replace('@', '')).attr('data-username');
      value = value.replace(match, '[~' + username + ']');
    }, this);
    this.$el.val(value);
  },

  checkInput: function (keyCode) {
    if (this._active) {
      this.checkActiveCode(keyCode);
    }
    if (keyCode === 50) {
      this._active = true;
      return;
    }
  },

  checkActiveCode: function (keyCode) {
    if (keyCode === 32) {
      this._active = false;
      this._initialized = false;
      this.$list.fadeOut('slow');
      return;
    }
    var term = this.getActiveTxt();
    if (!term) {
      return;
    }
    if (keyCode === 8 && term.length <= 3) {
      this._initialized = false;
    }
    if (term.length >= 3) {
      if (!this._initialized) {
        this.collection.fetch({
          data: { term: term }
        });
        this._initialized = true;
      } else {
        this.filter(term);
      }
    }
  },

  filter: function (s) {
    var re = new RegExp(s, 'i');
    this.collection.each(function (model) {
      var view = $('li[data-resultId="' + model.get('id') + '"]');
      if (!re.test(model.get('label'))) {
        view.hide();
      } else {
        view.show();
      }
    }, this);
  },

  getActiveTxt: function () {
    var value = this.$el.val();
    var start = this.currentMarkerPosition();
    var stop = this.getCaretPosition();
    return value.slice(start, stop);
  },

  getCaretPosition: function () {
    return this.$el[0].selectionStart;
  },

  currentMarkerPosition: function () {
    return this.$el.val().lastIndexOf('@') + 1;
  },

  displayResults: function () {
    this.$list.empty().hide();
    var offset = this.$el.offset();
    var pos = getCaretCoordinates(this.el, this.currentMarkerPosition());
    this.$list.css({
      top: pos.top + 20,
      left: pos.left
    });
    this.collection.each(function (item) {
      this.displayResult(item);
    }, this);
    this.$list.fadeIn('slow');
  },

  displayResult: function (item) {
    var result = new ResultView({ model: item });
    $(result.render().el).appendTo(this.$list);
    this.listenTo(result, 'activate', this.triggerCallback);
  },

  triggerCallback: function (model) {
    var start = this.currentMarkerPosition() - 1;
    var value = this.$el.val();
    this.$el.val(value.slice(0, start) + '[~' + model.get('value') + ']');
    this.$list.fadeOut('fast');
    this._active = false;
    this._initialized = false;
    this.$el.focus();
  }
});

return ActiveArea;

});
