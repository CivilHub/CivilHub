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

// Main object that handles scripts for voting buttons and bind counters.
// Constructor takes jQuery DOM element, which makes it easy to wrap function
// into plugin.

function VoteArea ($el) {
  this.$el = $el;
  this.activeBtn = null;
  this.counter = this.$el.find('.counter');
  this.counterup = this.$el.find('.counterup');
  this.note = this.$el.find('.note');
  _.bindAll(this, 'showMessage');
  this.$buttons = this.$el.find('.vote-btn-active');
  this.$buttons.on('click', function (e) {
    e.preventDefault();
    this.activeBtn = $(e.target);
    var id = this.activeBtn.attr('data-target-id');
    var vote = this.activeBtn.attr('data-vote');
    this.sendVote(id, vote, this.showMessage);
  }.bind(this));
}

// Make POST request and find out what the results are.

VoteArea.prototype.sendVote = function (id, vote, fn) {
  var data = { csrfmiddlewaretoken: utils.getCookie('csrftoken'), vote: vote };
  $.post('/ideas/vote/' + id + '/', data, fn);
};

// Show message with action summary and (if vote is positive) window to share.
// This function should run as callback, when we know, what the vote and voted
// objects states are.

VoteArea.prototype.showMessage = function (response) {
  ui.message.success(response.message);
  this.activeBtn
    .attr('data-vote', response.target)
    .text(response.label);
  this.counter.text(response.vote.count);
  this.counterup.text(response.vote.votes_up);
  this.note.text(response.vote.note);
  if (!_.isUndefined(response.old_label)) {
    this.$buttons.not(this.activeBtn)
      .attr('data-vote', response.old_target)
      .text(response.old_label);
  }
  if (response.vote.vote === true && response.target === 'revoke') {
    openShareWindow();
  }
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
