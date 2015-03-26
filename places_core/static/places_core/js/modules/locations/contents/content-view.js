//
// content-view.js
// ===============

// A single element view for a paginable collection
// that supports filters and lazy-loader.

define(['underscore', 'backbone', 'js/modules/utils/utils'],

function (_, Backbone, utils) {
    
  "use strict";
  
  var ContentView = Backbone.View.extend({
      
    tagName: 'div',
    
    className: 'col-sm-4 locBoxH',
    
    template: _.template($('#content-item-tpl').html()),
    
    render: function () {
      var imgUrl = utils.isRetina() ? this.model.get('retina_thumbnail')
                                    : this.model.get('thumbnail');
      this.$el.html(this.template(this.model.toJSON()));
      this.$('.locBoxIcon').find('a').tooltip();
      this.$('.locBoxHeader:first')
        .css('background-image', "url(" + imgUrl + ")");
      return this;
    }
  });
  
  return ContentView;
});