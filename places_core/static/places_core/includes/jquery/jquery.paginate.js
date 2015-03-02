/*
 * jquery.paginate.js
 * 
 * Simple jQuery pagination plugin made to be used with different template
 * pagination systems. It simply covers elements, that should not be visible
 * when there is too many pages to display.
 * 
 * Plugin provides callback method to be used with other applications, as well
 * as API hooks that allows developer to contol it's state programatically.
 * See README for details.
 */

(function ($) {

  "use strict";

  $.fn.pagination = function (options) {

    var defaults = {

      // First selected page number
      defaultOffset: 1,

      // Maximum page numbers to show
      visibleEntries: 17,

      // Text to fill collapsed pages indicators
      fakeLinkText: '...',

      // Callback to call when page is clicked
      onChange: null
    };

    var options = $.extend(defaults, options);

    return $(this).each(function () {

      var $this = $(this);

      var pages = [];

      // Set data-offset parameter for each page to simplify navigation

      $this.children('li').each(function () {
        var offset = parseInt($(this).text(), 10);
        if (!isNaN(offset)) {
          pages.push(offset);
          $(this).attr('data-offset', offset)
            .addClass('paginate-link-regular');
          if ($(this).hasClass('active')) {
            options.defaultOffset = offset;
          }
        }
      });

      var paginator = {

        $el: $this,

        _currentOffset: options.defaultOffset,

        _first: Math.min.apply(null, pages),

        _last: Math.max.apply(null, pages),

        _setOffset: function (offset) {
          this._currentOffset = offset;
        },

        _calcOffset: function () {
          var diff = Math.round(options.visibleEntries / 2),
            entries = [],
            minOff = this._currentOffset - diff - 1,
            maxOff = this._currentOffset + diff - 2,
            i = (minOff > 0) ? minOff : 0;

          if (maxOff > this._last) maxOff = this._last;
          for (i; i < maxOff; ++i) {
            entries.push(i);
          }
          return entries;
        },

        _addFake: function (dir) {
          var $li = $(document.createElement('li')),
            $a = $(document.createElement('a'));
          $li.addClass('paginate-link-fake').append($a);
          $a.attr('href', '#').text(options.fakeLinkText);
          if (dir === 'next') {
            $li.insertBefore(this.$el.find('.paginate-link-regular:last'));
          } else {
            $li.insertAfter(this.$el.find('.paginate-link-regular:first'));
          }
        },

        setPage: function (offset) {
          offset = Number(offset) || options.defaultOffset;
          this.$el.find('.active')
            .removeClass('active');
          this.$el.find('.paginate-link-regular[data-offset="' + offset + '"]')
            .addClass('active');
          this._setOffset(offset);
          this.render();
        },

        render: function () {
          var visible = this._calcOffset();
          this.$el.find('.paginate-link-regular').not(':first').not(':last').each(
            function (idx) {
              if (visible.indexOf(idx) >= 0) {
                $(this).show();
              } else {
                $(this).hide();
              }
            }
          );
          
          // Add indicators to show that we have some hidden elements

          this.$el.find('.paginate-link-fake').empty().remove();

          if (Math.max.apply(null, visible) + 3 < this._last) {
            this._addFake('next');
          }
          if (Math.min.apply(null, visible) + 1 > this._first) {
            this._addFake('prev');
          }
        }
      };

      $this.data('paginator', paginator);

      // Allow users to pass callback function. We pass current offset and 
      // paginator instance itself as arguments. The latter could be useful
      // for client-side apps. Additionaly we pass-in also click event object.
      
      $this.find('.paginate-link-regular').on('click', function (e) {
        if (options.onChange !== undefined && typeof(options.onChange) === 'function') {
          options.onChange(e, $(this).attr('data-offset'), paginator);
        }
      });

      paginator.setPage();

    });
  };
})(jQuery);