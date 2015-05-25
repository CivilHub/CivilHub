//
// active-form.js
// ==============

// Provides search url for different content type lists.

require(['jquery', 'CUri'], function ($, CUri) {

"use strict";

function ActiveForm () {
  this.version = '0.0.2';
  this.element = document.getElementsByTagName('body')[0];
  this.uri = new CUri(document.location.href);
  this.initialize();
}

ActiveForm.prototype.initialize = function () {
  var form = this;
  var $search = $('#haystack-form');
  var re = null;

  // Prapare clickable elements

  $('.list-controller').each(function () {
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

  $search.on('submit', function (e) {
    e.preventDefault();
    form.setOption('haystack', $search.find('[type="text"]').val());
    form.submit();
  });
  re = new RegExp('haystack=');
  if (re.test(document.location.href)) {
    $search.find('[type="text"]').val(this.uri.params.haystack);
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

$(document).ready(function () {
  var form = new ActiveForm(
    document.getElementsByTagName('body')[0]
  );
});

});
