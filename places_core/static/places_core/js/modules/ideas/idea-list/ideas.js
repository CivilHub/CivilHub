/**
 * ideas.js
 * ========
 * Run idea list.
 */
require(['jquery',
         'js/modules/ideas/idea-list/ideaList'],

function ($, IdeaList) {
    
  "use strict";
    
    /*// Initialize list.
    // -------------------------------------------------------------------------
    var ideas = new IdeaList();
    
    //
    // Obsługa kliknięć.
    // -----------------
    // Po kliknięciu na aktywny link w formularzu ta funkcja
    // zbiera wybrane opcje i tworzy URL do przekierowania.
    //
    $('.list-controller').bind('click', function (e) {
        var selectedItem = $(this).attr('data-control');

        e.preventDefault();

        $('.active[data-control="' + selectedItem + '"]')
            .removeClass('active');
        $(this).addClass('active');

        ideas.filter();
    });
    //
    // Zapisanie formularza.
    // ---------------------
    // W taki sam sposób jak powyżej, łączymy submit formularza.
    //
    $('#haystack-form').bind('submit', function (e) {
        e.preventDefault();
        ideas.filter();
    });*/

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