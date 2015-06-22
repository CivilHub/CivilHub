//
// blessbox.js
// ===========

// Handles box with recommendations for different content types.

require(['jquery',
         'underscore',
         'backbone',
         'js/modules/utils/utils',
         'js/modules/ui/ui'],

function ($, _, Backbone, utils, ui) {

"use strict";

function send (data, fn, context) {
  data = data || {};
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post('/api-bless/bless/', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

var Priest = Backbone.View.extend({
  initialize: function (options) {
    var counter = parseInt(this.$('.counter').text(), 10);
    if (isNaN(counter)) {
      counter = 0;
    }
    Backbone.View.prototype.initialize.call(this, options);
    this.$('.bless-trigger').on('click', this.bless.bind(this));
    this.model = new Backbone.Model({
      ct: this.$('.bless-trigger').attr('data-ct'),
      pk: this.$('.bless-trigger').attr('data-pk'),
      counter: counter
    });
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

$(document).ready(function () {
  $('.blessbox').each(function () {
    var priest = new Priest({ el: this });
    $(this).data('priest', priest);
  });
});

});
