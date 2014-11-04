//
// create-poll.js
// ==============
//
// Scripts to handle creating new poll.

require(['jquery',
         'underscore',
         'jqueryui',
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
        this.$el.find('.delete-entry-btn').on('click', function (e) {
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
      
        $('#id_tags').tagsInput({
            autocomplete_url: '/rest/tags/',
        });
      
        $('.add-answer-btn').tooltip().bind('click', function (e) {
            e.preventDefault();
            createAnswer();
        });
    });
});