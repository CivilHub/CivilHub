/**
 * ideas.js
 * ========
 * Run idea list.
 */
require(['jquery',
         'js/modules/ideas/idea-list/ideaList'],

function ($, IdeaList) {
    
  "use strict";
    
  var contents = new IdeaList();

  var filterTextContent = function () {
    var $field = $('#haystack'),
      txt = $field.val();
    
    if (_.isUndefined(txt) || txt.length <= 1) {
      return "";
    }
    
    return txt;
  };

  var filterListContent = function () {
    var $sel = $('.list-controller'),
      opts = {},
      optType = null,
      optValue = null,
      haystack = filterTextContent();
  
    $sel.each(function () {
      var $this = $(this);
      
      if ($this.hasClass('active')) {
        optType = $this.attr('data-control');
        optValue = $this.attr('data-target');
        opts[optType] = optValue;
      }
    });
    
    if (haystack !== false) {
      opts['haystack'] = haystack;
    }
    
    return opts;
  };

  $(document).ready(function () {

    // Check if there is a better way to handle external events.

    $('#haystack-form').on('submit', function (e) {
      e.preventDefault();
      contents.filter(filterListContent());
    });

    $('.list-controller').on('click', function (e) {
      e.preventDefault();
      var selectedItem = $(this).attr('data-control');
      $('.active[data-control="' + selectedItem + '"]')
        .removeClass('active');
      $(this).addClass('active');
      contents.filter(filterListContent());
    });
  });
});