//
// create-poll.js
// ==============
//
// Scripts to handle creating new poll.

require(['jquery',
         'underscore',
         'jqueryui',
         'js/modules/editor/plugins/uploader',
         'redactor',
         'tagsinput'], 

function ($, _) {
  
  "use strict";
  
  var ActiveAnswer = function (id) {
    this.id = id || 0;
    this.$el = $('<div class="answer-entry"></div>');
    this.tpl = _.template($('#answer-entry-tpl').html());
  };
  
  ActiveAnswer.prototype.render = function () {
    this.$el.html(this.tpl({id: this.id}));
    this.$el.find('.delete-entry-btn').tooltip().on('click', function (e) {
      e.preventDefault();
      this.$el.fadeOut('slow', function () {
        this.$el.empty().remove();
      }.bind(this));
    }.bind(this));
    return this;
  };
  
  function createAnswer () {
    var id = $('.answer-entry').length + 1,
        a = new ActiveAnswer(id);
    
    $('#poll-answer-form').append(a.render().$el);
  };
  
  $(document).ready(function () {
    
    $('#id_title').focus();
  
    $('#id_question').redactor({
      buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link'],
      plugins: ['uploader']
    });

    $('#id_tags').tagsInput({
      autocomplete_url: '/rest/tags/',
      defaultText: gettext("Add tag")
    });
  
    $('.add-answer-btn').tooltip().bind('click', function (e) {
      e.preventDefault();
      createAnswer();
    });
  });
});