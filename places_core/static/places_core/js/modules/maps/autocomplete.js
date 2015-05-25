define(['jquery', 'underscore'], function ($, _) {
  
// Simplified autocomplete functionality to search for places - it allows
// users to find and select single location to browse markers from.

// TODO: setLocation method should be universal, the same applies to the template
// TODO: timeout for 'keyup' event

$.fn.autocomplete = function (options) {
  
  var defaults = {
    // Clicking from a list of hints 
    onSelect: function (data) {console.log(data);},
    // Input field clear
    onClear: function () {console.log("Input clear");}
  };
    
  return $(this).each(function () {
    
    var $input = $(this),
      opts = _.extend(defaults, options),
      $ul = $('<ul class="custom-autocomplete"></ul>'),
      tpl = ['<li><a href="#" data-location="{id}" data-lat="{lat}"',
            ' data-lng="{lng}">{name}</a></li>'].join('');
    
    function clearItems () {
      $ul.find('li').empty().remove();
    }
    
    function toggleList () {
      if ($ul.find('li').length >= 1) {
        $ul.toggle();
      }
    }
    
    // FIXME: this should be a universal function
    
    function setLocation (data) {
      clearItems();
      $.each(data.results, function (idx, item) {
        var $li = $(tpl.replace(/{id}/g, item.id)
                 .replace(/{name}/g, item.name)
                 .replace(/{lat}/g, item.latitude)
                 .replace(/{lng}/g, item.longitude));
        $li.appendTo($ul);
        $li.find('a').on('click', function (e) {
          e.preventDefault();
          $input.val($(this).text());
          clearItems();
          // Fire callback onSelect()
          if (typeof(opts.onSelect === 'function')) {
            opts.onSelect($(this).data());
          }
        });
      });
    }
           
    $ul.insertAfter($input);
    
    $input.on('keyup', function () {
      
      if ($input.val().length === 0) {
        // Fire callback onClear()
        if (typeof(opts.onClear) === 'function') {
          opts.onClear();
        }
        return false;
      }
      
      $.get('/api-locations/markers/',{term:$input.val()},setLocation);
    });
    
    $input.on('click', toggleList);
  });
};

});
