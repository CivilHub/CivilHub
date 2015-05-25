//
// content-view.js
// ===============

// A single element view for a paginable collection
// that supports filters and lazy-loader.

define(['underscore', 'backbone', 'js/modules/utils/utils'],

function (_, Backbone, utils) {

  "use strict";

  var ContentView = Backbone.View.extend({

    className: 'timeline-item',

    tagName: 'li',

    template: _.template($('#content-item-tpl-new').html()),

    render: function () {
      var imgUrl = utils.isRetina() ? this.model.get('retina_thumbnail')
                                    : this.model.get('thumbnail');
      this.$el.html(this.template(this.model.toJSON()));
      this.$('.date').tooltip();
      this.$('.timeline-image:first')
        .css('background-image', "url(" + imgUrl + ")");
      return this;
    }
  });

  return ContentView;
});
