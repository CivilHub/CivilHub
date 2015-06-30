//
// vote-area.js
// ============

// Handle votes for ideas.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/utils',
        'js/modules/ui/ui',
         'text!js/modules/ideas/templates/share-modal.html',
        'bootstrap'],

function ($, _, Backbone, utils, ui, html) {

"use strict";

var APIURL = '/api-ideas/ideas/';
var TPLURL = '/ideas/vote-form/';

function sendVote (data, fn, ctx) {
  var id = data.id;
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post(APIURL + id + '/vote/', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(ctx, response);
    }
  });
}

function fetch (id, vote, fn, ctx) {
  $.get(TPLURL + id + '/' + vote + '/', function (response) {
    if (_.isFunction(fn)) {
      fn.call(ctx, response);
    }
  });
}

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

var VoteArea = Backbone.View.extend({

  events: {
    'click .vote-btn': 'prepareVote'
  },

  initialize: function (options) {
    this.model = new Backbone.Model({
      id: this.$el.attr('data-target-id')
    });
    this.$('.modal').modal({ show: false });
    this.$buttons = this.$('.vote-btn');
  },

  prepareVote: function (e) {
    e.preventDefault();
    var $btn = $(e.currentTarget);
    var vote = $btn.attr('data-vote');
    var data = { id: this.model.get('id'), vote: vote };
    this._active = $btn;
    if (vote == 3) {
      sendVote(data, this.commitVote, this);
      return;
    }

    this.getForm(vote);

    this.$('.modal').modal('show');
    this.$('.submit-btn').one('click', function (e) {
      e.preventDefault();
      data.comment = this.$('textarea').val();
      sendVote(data, this.commitVote, this);
    }.bind(this));

    this.$('.modal').on('hidden.bs.modal', function () {
      this.$('.submit-btn').off('click');
    }.bind(this));
  },

  getForm: function (vote) {
    var v = vote || 2;
    var heading = "";
    fetch(this.model.get('id'), v, function (response) {
      this.$('.modal-body').html(response);
      if (vote == 1) {
        heading = gettext("How can you help?");
      } else {
        heading = gettext("Reason");
      }
      this.$('.modal-title').text(heading);
    }, this);
  },

  commitVote: function (data) {
    if (!data.result.success) {
      this.displayErrors(data.result);
    } else {
      this.showResults(data.result);
      this.$('.modal').modal('hide');
    }
  },

  displayErrors: function (data) {
    this.$('.modal').find('.alert')
      .text(data.error).fadeIn('fast');
  },

  showResults: function (data) {
    console.log(data);
    this.$('.counter').text(data.votes);
    this.$('.note').text(data.note);
    if (data.is_reversed) {
      this.$buttons.not(this._active).text(data.new_label);
    } else if (!_.isNull(data.prev_target)) {
      this._active.attr('data-vote', data.prev_target);
    }
    this._active.text(data.label);
    ui.message.success(data.message);
    if (data.target == 1) {
      openShareWindow();
    }
  }
});

return VoteArea;

});
