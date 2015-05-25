//
// actionView.js
// =============
//
// Single action entry view.

define(['underscore', 'backbone', 'moment'],

function (_, Backbone, moment) {

  "use strict";

  var ActionView = Backbone.View.extend({

    id: 'tour-activity',

    tagName: 'li',

    className: 'timeline-item',

    template: _.template($('#action-template-new').html()),

    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      this.$('.date').tooltip();
      return this;
    }
  });

  return ActionView;
});
