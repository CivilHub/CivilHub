//
// votes.js
// ========

// App to manage idea votes.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'js/modules/ideas/votes/counterWindow',
         'text!js/modules/ideas/templates/share-modal.html'],

function ($, _, utils, ui, CounterWindow, html) {

"use strict";

// A window with vote summary.

var cw = null;

function send (id, data, fn, context) {
  data = data || {};
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post('/ideas/vote/' + id + '/', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

$(document).ready(function () {
  $('.idea-vote-count').on('click', function (e) {
    e.preventDefault();
    cw = new CounterWindow({
      ideaId: $(this).attr('data-target')
    });
  });
});

// Share content after voting

function openShareWindow () {
  var tpl = _.template(html);
  var $el = $(tpl({
    token: CivilApp.fbClientToken,
    url: document.location.href,
    title: document.title
  }));
  $el.modal();
  $el.find('.trigger-link').on('click', function (e) {
    e.preventDefault();
    window.open($(this).attr('href'), $(this).text(),
      "width=600,height=350,menubar=0,status=0,resizable=1");
  });
  $el.find('a').on('click', function (e) {
    e.preventDefault();
    $el.modal('hide');
  });
}

function VoteArea ($el) {
  this.$el = $el;
  this.$activeBtn = null;
  this.$buttons = this.$el.find('.vote-btn-active');
  this.$counter = this.$el.find('.counter');
  this.$note = this.$el.find('.note');
  this.$buttons.on('click', this.trigger.bind(this));
}

VoteArea.prototype.trigger = function (e) {
  e.preventDefault();
  this._active = $(e.target);
  var idea = this._active.attr('data-target-id');
  var vote = this._active.attr('data-vote');
  send(idea, { vote: vote }, this.showSummary, this);
};

VoteArea.prototype.showSummary = function (data) {
  if (data.is_reversed) {
    this.$buttons.not(this._active).text(data.new_label);
  } else {
    this._active.attr('data-vote', data.prev_target);
  }
  this._active.text(data.label);
  this.$counter.text(data.votes);
  this.$note.text(data.note);
  ui.message.success(data.message);
};

// jQuery wrapper for VoteArea

$.fn.voteArea = function () {
  return $(this).each(function () {
    var area = new VoteArea($(this));
    return this;
  });
};

$(document).ready(function () {
  if (_.isNull(CivilApp.currentUserId)) {
    return;
  }
  $('.vote-form').voteArea();
});

});
