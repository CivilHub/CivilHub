/**
 * content-view.js
 * ===============
 *
 * Widok pojedynczego elementu dla paginowalnej
 * kolekcji obsługującej filtry i lazy-loader.
 */
define(['underscore', 'backbone'],

function (_, Backbone) {
    
  "use strict";
  
  var ContentView = Backbone.View.extend({
      
    tagName: 'div',
    
    className: 'col-sm-4 locBoxH',
    
    template: _.template($('#content-item-tpl').html()),
    
    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }
  });
  
  return ContentView;
});