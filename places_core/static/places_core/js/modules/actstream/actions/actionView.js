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
      
    tagName: 'div',
    
    className: 'row action-entry',
    
    template: _.template($('#action-template').html()),
    
    render: function () {
      this.$el.html(this.template(this.model.toJSON()));  
      this.$('.actiClock').find('span').tooltip();    
      return this;
    }
  });
  
  return ActionView;
});