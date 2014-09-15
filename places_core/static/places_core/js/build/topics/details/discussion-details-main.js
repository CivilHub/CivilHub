//
// Widok pojedynczej dyskusji
//
//  => /templates/topics/discussion_detail.html
//
// --------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
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
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
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
         'js/ui/ui',
         'js/maps/minimap',
         'js/ui/mapinput',
         'js/common',
         'js/ui/bookmark-form',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/topics/reply-form',
         'js/topics/category-creator'],

function ($, ui, Minimap) {
    
    "use strict";
    
    $(document).ready(function () {
        var minimap = new Minimap(window.MARKERS);
        $('.minimap-toggle-button').on('click', function (e) {
            e.preventDefault();
            minimap.open();
        });
    });
    
    $('.map-marker-toggle').bind('click', function (evt) {
        evt.preventDefault();
        
        var $modal   = $(_.template($('#map-marker-form-template').html(), {})),
            $form    = $modal.find('form:first'),
            $submit  = $modal.find('.submit-btn:first'),
            formData = {};
            
        $modal.modal('show');
        
        $modal.on('shown.bs.modal', function () {
            
            $('#id_latitude').before('<div id="map"></div>');
            $('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 550,
                height: 300
            });
            
            $form.on('submit', function (evt) {
                evt.preventDefault();
            });
            
            $submit.on('click', function () {
                formData = {
                    content_type: $('#id_content_type').val(),
                    object_pk   : $('#id_object_pk').val(),
                    latitude    : $('#id_latitude').val(),
                    longitude   : $('#id_longitude').val()
                }
                
                $.ajax({
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    type: 'POST',
                    url: $form.attr('action'),
                    data: formData,
                    dataType: 'json',
                    success: function (resp) {
                        ui.message.success(resp.message);
                    },
                    error: function (err) {
                        console.log(err);
                    }
                });
                
                $modal.modal('hide');
            });
        });
        
        $modal.on('hidden.bs.modal', function () {
            $modal.empty().remove();
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
        });
    });
    
    //
    // Save user's vote on server
    // --------------------------
    // @param {boolean} vote
    // @param {string} url
    // @param {jQuery Object} $counter
    //
    var sendVote = function (vote, url, $counter) {
        var votes = parseInt($counter.text(), 10) || 0;
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                vote: vote,
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]:first').val()
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success) {
                    message.success(resp.message);
                    $counter.text(++votes);
                } else {
                    message.warning(resp.message);
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    };
    
    $('.entry-vote-up').on('click', function (e) {
        e.preventDefault();
        var vote = true;
        var url = $(this).attr('href');
        var $counter = $(this).siblings('.entry-vote-count');
        sendVote(vote, url, $counter);
    });
    
    $('.entry-vote-down').on('click', function (e) {
        e.preventDefault();
        var vote = false;
        var url = $(this).attr('href');
        var $counter = $(this).siblings('.entry-vote-count');
        console.log($counter);
        sendVote(vote, url, $counter);
    });
    
    // Abuse reports for entries
    // ---------------------------------------------------------------------
    var AbuseModel = Backbone.Model.extend({
        defaults: {
            comment: "",
            content_type: 0,
            content_label: "",
            object_pk: 0,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }
    });
    
    var AbuseWindow = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'modal fade',
        
        template: _.template($('#abuse-window-tpl').html()),
        
        events: {
            'click .submit-btn': 'sendReport'
        },
        
        initialize: function (data) {
            this.model = new AbuseModel(data);
            this.render();
            this.$el.modal({show:false});
        },
        
        render: function () {
            var self = this;
            this.$el.html(this.template(this.model.toJSON()));
            this.$form = this.$el.find('form:first');
            this.$el.on('hidden.bs.modal', function () {
                self.destroy();
            });
        },
        
        open: function () {
            this.$el.modal('show');
        },
        
        close: function () {
            this.$el.modal('hide');
        },
        
        destroy: function () {
            this.$el.empty().remove();
        },
        
        sendReport: function () {
            $.ajax({
                type: 'POST',
                url: '/rest/reports/',
                data: this.$form.serializeArray(),
                success: function (resp) {
                    console.log(resp);
                    message.success(gettext("Report sent"));
                },
                error: function (err) {
                    console.log(err);
                    message.alert(gettext("An error occured"));
                }
            });
            this.close();
        }
    });

    $(document).delegate('.report-abuse-entry-link', 'click', function (e) {
        e.preventDefault();
        var $toggle = $(this);
        console.log($toggle);
        var win = new AbuseWindow({
            content_type: $toggle.attr('data-content'),
            content_label: $toggle.attr('data-label'),
            object_pk: $toggle.attr('data-id')
        });
        win.open();
        console.log(getCookie('csrftoken'));
    });
    
    $(document).trigger('load');
    
});