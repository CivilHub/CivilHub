//
// progress.js
// ===========

// Simple script that binds form with checkboxes with Bootstrap progress bar.
// Simply choose the name of checkbox group to make it work.

define(['jquery',
        'underscore'],

function ($, _) {

"use strict";

var template = '<div class="progress"><div class="progress-bar"' +
               ' role="progressbar" aria-valuenow="0" aria-valuemin="0"' +
               ' aria-valuemax="100" style="width: 0%;">0%</div></div>';

function ProgressForm (name) {
  this.$controls = $('[name="' + name + '"]');
  this.$progress = $(template);
  this.$progress.insertBefore(
    this.$controls.parents('.task-container:first')
  );
  _.bindAll(this, 'checkValues');
  this.$controls.on('click', this.checkValues);
  this.checkValues();
}

ProgressForm.prototype.checkValues = function () {
  var checked = 0;
  var unchecked = 0;
  var value = 0;
  _.each(this.$controls, function (item) {
    if ($(item).is(':checked')) {
      ++checked;
    } else {
      ++unchecked;
    }
  }, this);
  value = parseInt(checked / (checked + unchecked) * 100, 10);
  this.$progress
    .find('.progress-bar')
    .css('width', value + '%')
    .text(value + '%');
};

return ProgressForm;

});
