//
// Strona wyświetlania wyników ankiety => /templates/polls/poll-results.html
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        ckeditor: 'includes/ckeditor/ckeditor',
        dropzone: 'includes/dropzone/dropzone',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        tagsinput: 'includes/jquery/jquery.tagsinput'
    },
    
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore'],
            exports: 'Backbone'
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        tagsinput: {
            deps: ['jquery']
        },
        
        ckeditor: {
            exports: 'CKEDITOR'
        },
        
        dropzone: {
            deps: ['jquery'],
            exports: 'Dropzone'
        },
        
        jqueryui: {
            deps: ['jquery']
        },
        
        tagsinput: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'underscore',
         'bootstrap',
         'tagsinput',
         'js/editor/customCKEditor',
         'common'],

function ($, _) {
    
    "use strict";
    
    $('#id_question').customCKEditor('custom');
    $('#id_title').focus();
    $('#id_tags').tagsInput({
        autocomplete_url: '/rest/tags/',
    });
    function ActiveAnswer (id) {
        return {
            id: id,
            $el: $('<div class="answer-entry"></div>'),
            tpl: _.template($('#answer-entry-tpl').html()),
            render: function () {
                var _that = this;
                _that.$el.html(_that.tpl({id: id}));
                _that.$el.find('.delete-entry-btn').on('click', function (evt) {
                    evt.preventDefault();
                    _that.$el.fadeOut('slow', function () {
                        _that.$el.empty().remove();
                    });
                });
                return _that.$el;
            }
        }
    }
    function createAnswer () {
        var id = $('.answer-entry').length + 1,
            a = new ActiveAnswer(id);
        $('#poll-answer-form').append(a.render());
    }
    $('.add-answer-btn').tooltip().bind('click', function (evt) {
        evt.preventDefault();
        createAnswer();
    });
    
    $(document).trigger('load');
    
});