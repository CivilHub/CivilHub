//
// location-delete.js
// ==================

// Delete location page. Here we have some autocomplete to help us find other
// locations to which we may need to move contents from deleted place.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'underscore',
           'jqueryui',
           'js/modules/common',
           'js/modules/locations/follow'],

  function ($, _) {

    "use strict";

    var template = _.template($('#autocomplete-item-tpl').html());

    $(document).ready(function () {
      $('#location-autocompleter').autocomplete({
        minLength: 3,
        source: "/places/",
        response: function (e, ui) {
          $('#autocompleter-results').empty();
          $.map(ui.content, function (item) {
            $(template(item)).appendTo('#autocompleter-results');
          });
        }
      });
    });

    $(document).trigger('load');

  });

});
