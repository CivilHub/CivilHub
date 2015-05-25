//
// abuse-report.js
// ===============

// Allow registered users to send abuse reports related to content.

define(['jquery',
        'underscore',
        'js/modules/ui/ui',
        'js/modules/utils/utils',
        'bootstrap'],

function ($, _, ui, utils) {

"use strict";

function getFormTemplate (url, context, callback) {
  $.get(url, function (response) {
    callback.call(context, response);
  });
}

function sendReport (url, data, context, callback) {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': utils.getCookie('csrftoken') }
  });
  $.post(url, data, function (response) {
    callback.call(context, response);
  });
}

function AbuseWindow (ct, pk) {
  this.baseUrl = (['/report', ct, pk]).join('/') + '/';
  getFormTemplate(this.baseUrl, this, function (response) {
    this.initialize(response);
  });
}

AbuseWindow.prototype.close = function () {
  this.$el.empty().remove();
  $('.modal-backdrop').empty().remove();
};

AbuseWindow.prototype.displayErrors = function (errors) {
  for (var err in errors) {
    if (hasOwnProperty(errors, err)) {
      this.$el.append('<p>' + err[0] + '</p>');
    }
  }
};

AbuseWindow.prototype.initialize = function (html) {
  this.$el = $(html);
  this.$form = this.$el.find('form:first');
  this.$submit = this.$el.find('[type="submit"]:first');
  this.$el.appendTo('body').modal();
  this.$el.on('hidden.bs.modal', function () {
    this.close();
  }.bind(this));
  this.$submit.on('click', function (e) {
    e.preventDefault();
    this.send();
  }.bind(this));
};

AbuseWindow.prototype.send = function () {
  var attrs = {};
  _.each(this.$form.serializeArray(), function (field) {
    attrs[field.name] = field.value;
  });
  sendReport(this.baseUrl, attrs, this, function (response) {
    if (response.success) {
      ui.message.success(response.message);
      this.close();
    } else {
      this.displayErrors(response.errors);
    }
  });
};

return AbuseWindow;

});
