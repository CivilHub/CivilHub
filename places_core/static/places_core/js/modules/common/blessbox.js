//
// blessbox.js
// ===========

// Handles box with recommendations for different content types.

require(['jquery',
         'underscore',
         'backbone',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'bootstrap'],

function ($, _, Backbone, utils, ui) {

"use strict";

// Misc utils and helper functions
// -----------------------------------------------------------------------------

/** basic template */

var TPL = '<li><img src="<%= user.profile.thumbnail %>" alt="<%= user.full_name %>">' +
          '<a href="<%= user.profile.url %>"><%= user.full_name %></a></li>';

/**
 * Get list of all recommendations from server.
 * @param {object} URL parameters
 * @param {function} Callback to trigger on success
 * @param {object} Context variable to pass as 'this' for callback
 */
function fetch (data, fn, ctx) {
  $.get('/api-bless/recommendations/', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(ctx, response);
    }
  });
}

/**
 * Create or delete existing recommendation by performin POST request.
 * @param {object} URL parameters
 * @param {function} Callback to trigger on success
 * @param {object} Context variable to pass as 'this' for callback
 */
function send (data, fn, context) {
  data = data || {};
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post('/api-bless/bless/', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

// Backbone views
// -----------------------------------------------------------------------------

/** Simple view wrapper for single list item in summary window. */

var Bless = Backbone.View.extend({

  template: _.template(TPL),

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  }
});

/** Show summary with all recommendations in modal window. */

var Church = Backbone.View.extend({

  initialize: function (options) {
    this.meta = { ct: options.ct, pk: options.pk };
    this.$el.modal({ show: false });
  },

  show: function () {
    fetch(this.meta, function (response) {
      this.render(response);
      this.open();
    }, this);
  },

  render: function (data) {
    var $list = $('<ul></ul>');
    this.$('.modal-body').empty().append($list);
    _.each(data, function (item) {
      var bless = new Bless({
        model: new Backbone.Model(item)
      });
      $(bless.render().el).appendTo($list);
    }, this);
  },

  open: function () {
    this.$el.modal('show');
  }
});

/** Handles entire 'blessbox' application. */

var Priest = Backbone.View.extend({
  initialize: function (options) {
    var counter = parseInt(this.$('.counter').text(), 10);
    if (isNaN(counter)) {
      counter = 0;
    }
    Backbone.View.prototype.initialize.call(this, options);
    this.$('.bless-trigger').on('click', this.bless.bind(this));
    this.model = new Backbone.Model({
      ct: this.$el.attr('data-ct'),
      pk: this.$el.attr('data-pk'),
      counter: counter
    });

    this.church = new Church({
      el: this.$('.modal'),
      ct: this.model.get('ct'),
      pk: this.model.get('pk')
    });

    this.$('.t-count').on('click', function (e) {
      e.preventDefault();
      this.church.show();
    }.bind(this));
  },

  bless: function (e) {
    e.preventDefault();
    var data = {
      ct: this.model.get('ct'),
      pk: this.model.get('pk')
    };
    send(data, function (response) {
      this.update(response);
    }, this);
  },

  update: function (data) {
    if (data.bless) {
      ui.message.success(gettext("Thank you for your recommendation") + "!");
    }
    this.$('.counter-body').html(data.message);
    this.$('.bless-trigger').find('.fa')
      .toggleClass('fa-heart-o')
      .toggleClass('fa-heart');
  }
});

// Run!
// -----------------------------------------------------------------------------

$(document).ready(function () {
  $('.blessbox').each(function () {
    var priest = new Priest({ el: this });
    $(this).data('priest', priest);
  });
});

});
