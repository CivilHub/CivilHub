//
// autocomplete.js
// ===============

// Simple autocomplete fetching userlist matching to entered search query.

// FIXME: most of this code is copied directly from active area plugin.
// Shuld try to add some options to plugin to make it working also here.

require(['jquery',
         'underscore',
         'backbone',
         'js/modules/utils/caret-position',
         'text!tpl/active-area/result.html'],

function ($, _, Backbone, getCaretCoordinates, resultHTML) {

"use strict";

var ResultCollection = Backbone.Collection.extend({
  url: '/api-userspace/mention/'
});

// Single result entry with profile picture and user ful name.

var ResultView = Backbone.View.extend({

  tagName: 'li',

  template: _.template(resultHTML),

  // Mark filtered out entries as 'hidden'.

  _hidden: false,

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    this.$el.attr('data-resultId', this.model.get('id'));
    this.$el.on('click', function (e) {
      this.trigger('activate', this.model);
    }.bind(this));
    return this;
  },

  // Show entry if it was hidden and match search phrase.

  show: function () {
    this.$el.show();
    this._hidden = false;
  },

  // Hide entry if user full name doesn't match search phrase.

  hide: function () {
    this.$el.hide();
    this._hidden = true;
  }
});

// Main object that holds entire area bind to single input
// entry (usually this will be textarea element).

var AutocompleteArea = Backbone.View.extend({

  // Marks plugin as active - searching etc. is enabled if true

  _active: true,

  // Marks plugin as initialized - usually we fetch
  // initial data only once and set this flag to true.

  _initialized: false,

  // Holds view elements bound with collection models via
  // ID attribute. Model's ID becomes key in this object.

  _items: {},

  // Marks plugin as 'waiting' when there is no more results to show.
  // User may either write regular text or press backspace to see list again.

  _waiting: false,

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

  // Replace initial input content with proper macros representaions.
  //
  // FIXME: find some more efficient way to replace mention links.

  replaceContent: function () {
    var re = new RegExp(/\@<a(.*?([\w-]+))<\/a>/g);
    var value = this.$el.val() || "";
    var res = value.match(re);
    var username = "";
    _.each(res, function (match) {
      username = $(match.replace('@', '')).attr('data-username');
      value = value.replace(match, username);
    }, this);
    this.$el.val(value);
  },

  // Check if input is already active and process it or activate plugin.

  checkInput: function (keyCode) {
    if (this._active) {
      this.checkActiveCode(keyCode);
    }
    if (keyCode === 32) {
      this._active = true;
      return;
    }
  },

  // This is core function that handles most of program logic.
  //
  // When plugin is active, this function checks, what key was pressed by user
  // and decide what to do next (either filter result list or deactivate plugin).

  checkActiveCode: function (keyCode) {

    // Special case of 'waiting' state. Here user can resign or press
    // backspace key to see result list again and keep it working.

    if (this._waiting) {
      switch (keyCode) {
        case 32:
          this._active = false;
          this._initialized = false;
          break;
        case 8:
          this.$list.fadeIn('fast');
          break;
      }
      this._waiting = false;
      return;
    }

    // If there is nothing to process, we obviously has nothing to do.

    var term = this.getActiveTxt();
    if (!term) {
      return;
    }

    // Fetch list again if user will back to 3 or less characters again.

    if (keyCode === 8 && term.length <= 3) {
      this._initialized = false;
    }

    // Check if search term is reasonably long and either fetch new results
    // from server or filter existing entries to match search query.

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

  // Narrow list to display only fields containing users that match search term.

  filter: function (s) {
    var re = new RegExp(s, 'i');
    this.collection.each(function (model) {
      var view = this._items[model.get('id')];
      if (!re.test(model.get('label'))) {
        view.hide();
      } else {
        view.show();
      }
    }, this);

    // Find out if suggestion list is already empty and hide plugin if so.

    var chk = _.every(this._items, function (item) {
      return item._hidden;
    });
    if (_.isEmpty(this._items)) chk = false;
    if (chk && this.getActiveTxt().length > 3) {
      this._waiting = true;
      this.$list.fadeOut('slow');
    }
  },

  // Returns currently processed macro text.

  getActiveTxt: function () {
    var value = this.$el.val();
    var start = this.currentMarkerPosition();
    var stop = this.getCaretPosition();
    return value.slice(start, stop);
  },

  // Helper that returns caret position inside input element.
  //
  // This is required for proper display position for result list.

  getCaretPosition: function () {
    return this.$el[0].selectionStart;
  },

  // Last marker that opened macro and initialized plugin.

  currentMarkerPosition: function () {
    var idx = this.$el.val().lastIndexOf(',');
    if (idx < 0) {
      return 0;
    }
    return idx + 2;
  },

  // Presents entire results list. Usually used only once on initial fetch.

  displayResults: function () {
    this.$list.empty().hide();
    var offset = this.$el.offset();
    var pos = getCaretCoordinates(this.el, this.currentMarkerPosition());
    this.$list.css({
      top: pos.top + 50,
      left: pos.left
    });
    this.collection.each(function (item) {
      this.displayResult(item);
    }, this);
    this.$list.fadeIn('slow');
  },

  // Create single result view object and append it to DOM.

  displayResult: function (item) {
    var result = new ResultView({ model: item });
    $(result.render().el).appendTo(this.$list);
    this.listenTo(result, 'activate', this.triggerCallback);

    // Bind view and model in inner plugin registry.

    this._items[item.id] = result;
  },

  // Final function when user selected some position.
  //
  // Creates proper macro based on selected entry and
  // replaces input value accordingly.

  triggerCallback: function (model) {
    var start = this.currentMarkerPosition();
    var value = this.$el.val();
    this.$el.val(value.slice(0, start) + model.get('value') + ', ');
    this.$list.fadeOut('fast');
    this._initialized = false;
    this.$el.focus();
  }
});

$(document).ready(function () {
  $('.active-input').each(function () {
    var aa = new AutocompleteArea({ el: this });
    $(this).data('AutocompleteArea', aa);
  });
});

});
