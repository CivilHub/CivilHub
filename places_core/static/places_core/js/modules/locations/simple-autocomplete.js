//
// simple-autocomplete.js
// ======================

// Scripts dedicated for location_autocomplete template tag.

require(['jquery',
         'underscore',
         'backbone',
         'js/modules/locations/follow-button',
         'jqueryui'],

function ($, _, Backbone, fb) {

"use strict";

function getTemplate (model) {
  if (model.get('template') === 'simple') {
    return _.template($('.actl-tpl-simple').html());
  }
  if (model.get('following')) {
    return _.template($('.actl-tpl-followed').html());
  }
  return _.template($('.actl-tpl').html());
}

var AutocompleteResult = Backbone.View.extend({

  initialize: function (options) {
    this.template = getTemplate(this.model);
  },

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    this.$('.btn-follow, .btn-unfollow').on('click', this.toggle.bind(this));
    return this;
  },

  toggle: function (e) {
    var $btn = $(e.currentTarget);
    fb.followRequest(this.model.get('value'), function (response) {
      $btn.text(fb.settext(response.following))
        .toggleClass('btn-follow-location')
        .toggleClass('btn-unfollow-location');
    });
  }
});

var CivAutocomplete = Backbone.View.extend({
  initialize: function (options) {
    var $list = this.$('.autocomplete-results');
    var $input = this.$('.civ-autocomplete');
    $input.autocomplete({
      minLength: 4,
      source: "/api-locations/autocomplete/",
      response: function (e, ui) {
        $list.empty();
        $.map(ui.content, function (item) {
          var result = new AutocompleteResult({
            model: new Backbone.Model(item)
          });
          $(result.render().el).appendTo($list);
        });
      }
    });
  }
});

$(document).ready(function () {
  $('.civ-autocomplete-area').each(function () {
    var autocomplete = new CivAutocomplete({ el: this });
  });
});

});
