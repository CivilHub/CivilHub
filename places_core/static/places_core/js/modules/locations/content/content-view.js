/**
 *
 */

define(['underscore', 'backbone'],

function (_, Backbone) {
    
  "use strict";
  
  var ActionView = Backbone.View.extend({
      
    tagName: 'div',
    
    className: 'col-sm-4 locBoxH',
    
    template: _.template($('#content-item-tpl').html()),
    
    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }
  });
  
  return ActionView;
});