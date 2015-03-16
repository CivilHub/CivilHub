//
// active-form.js
// ==============

// Filtrowanie list różnych typów zawartości.

require(['jquery', 'CUri'], function ($, CUri) {

  "use strict";

  function ActiveForm (element, url) {
    url = url || document.location.href;
    this.version = '0.0.1';
    this.element = element;
    this.uri = new CUri(url);
    this.initialize();
  }

  ActiveForm.prototype.initialize = function () {
    var form = this;
    var $search = $(this.element).find('[type="text"]');
    var re = null;

    // Prapare clickable elements

    $(this.element).find('.list-controller').each(function () {
      $(this).on('click', function (e) {
        e.preventDefault();
        form.setOption(
          $(this).attr('data-control'),
          $(this).attr('data-target')
        );
        form.submit();
      });
      re = new RegExp(([
        $(this).attr('data-control'),
        $(this).attr('data-target')]).join('=')
      );
      if (re.test(document.location.href)) {
        $(this).addClass('active');
      } else {
        $(this).removeClass('active');
      }
    });

    // Prepare search form

    $(this.element).find('form').on('submit',
      function (e) {
        e.preventDefault();
        form.setOption('haystack', $search.val());
        form.submit();
      }
    );
    re = new RegExp('haystack=');
    if (re.test(document.location.href)) {
      $search.val(this.uri.params.haystack);
    }
  };

  ActiveForm.prototype.setOption = function (option, value) {
    this.uri.add(option, value);
  };

  ActiveForm.prototype.reset = function () {
    this.uri.clear();
  };

  ActiveForm.prototype.submit = function () {
    document.location.href = this.uri.url();
  };

  $.fn.activeForm = function () {
    return $(this).each(function () {
      var form = new ActiveForm(this, null);
      $(this).data('activeForm', form);
    });
  };

  $(document).ready(function () {
    $('#filter-navbar').activeForm();
  });
});