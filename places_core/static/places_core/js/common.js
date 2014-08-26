//
// common.js
// =========
//
// Simple common scripts, such as tooltips etc.
//
define(['jquery',
        'underscore',
        'backbone',
        'bootstrap',
        'js/ui/bookmark-form'],

function ($, _, Backbone) {
    
    "use strict";
    
    window.getCookie = function (name) {
        "use strict";
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };    
    
    (function($) {
        if(!getCookie('cookie_msg')) {
        
            $('#cookie-msg').prepend('<div class="alert fade in fade out">' + gettext('Pliki cookie pomagają nam udostępniać nasze usługi. Korzystając z tych usług, zgadzasz się na użycie plików cookie') + '.' + '<a class="btn" href="/cookies">' + gettext("Polityka cookies") + '</a><a id="accept-button" class="btn" data-dismiss="alert">OK</a></div>')
                .hide().fadeIn('slow');
            
            $('#accept-button').click(function () {
                var expiration_date = new Date();
                expiration_date.setFullYear(expiration_date.getFullYear() + 1);
                document.cookie = "cookie_msg=true; path=/; expires=" + expiration_date.toGMTString();
                $('#cookie-msg').fadeOut('slow', function() {
                    this.empty().remove();
                });
            });
        }
    })(jQuery);
    
    $("#lang-selector").popover({
        html : true, 
        content: function() {
          return $('#popover-lang-list').html();
        },
        
        placement: "top"
    });
    /*$('#lang-selector').bind('click', function (evt) {
        var $toggle     = $(this),
            $submenu    = $toggle.find('ul');

        if ($submenu.attr('data-opened') === undefined) {
            $submenu
                .slideDown('fast')
                .attr('data-opened', true)
                .offset({
                    left: $toggle.offset().left,
                    top:  $toggle.offset().top + $toggle.height() - $submenu.height()
                });
        } else {
            $submenu
                .slideUp('fast')
                .removeAttr('data-opened');
        }
    });*/
    
    //
    // Abuse reports
    // -------------------------------------------------------------------------
    
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
    
    //
    // Handle abuse reports for regular content on single view page.
    //
    $(document).delegate('.report-abuse-link', 'click', function (e) {
        e.preventDefault();
        var reportWindow = new AbuseWindow({
            content_type: $('#target-type').val(),
            content_label: $('#target-label').val(),
            object_pk: $('#target-id').val()
        });
        reportWindow.open();
    });
    
    //
    // Tag Cloud
    // -------------------------------------------------------------------------
    
    var max_counter = 0,
        i = 0,
        min_counter, avg;

    $('.tags > ul > li').each(function () {
        // Zbieramy wartości counterów dla każdego taga.
        var count = parseInt($(this).attr('data-counter'), 10);
        if (count > max_counter) {
            max_counter = count;
        }
        if (min_counter == undefined || count < min_counter) {
            min_counter = count;
        }
        i++
    });

    $('.tags > ul > li').each(function () {
        // Kolejna pętla - przyporządkujemy klasy na podstawie
        // zebranych wcześniej wartości.
        var count = parseInt($(this).attr('data-counter'), 10);
        
        if (count <= max_counter / 5) {
            $(this).addClass('tag1');
        } else if (count <= max_counter / 4) {
            $(this).addClass('tag2');
        } else if (count <= max_counter / 3) {
            $(this).addClass('tag3');
        } else if (count <= max_counter / 2) {
            $(this).addClass('tag4');
        } else {
            $(this).addClass('tag5');
        }
    });
    
    // Common simple scripts.
    // -------------------------------------------------------------------------
    // Errorlist custom styles.
    $('.errorlist > li').addClass('alert alert-danger');
    // Cancel button for some forms which allow back one page.
    $('.cancel-btn').on('click', function () {
        history.go(-1);
    });
    // Tooltips for elements shared among templates.
    $('.navbar-avatar').tooltip({placement: 'bottom'});
    $('.custom-tooltip').tooltip();
    $('.custom-tooltip-bottom').tooltip({
        placement: 'bottom'
    });
    // Bookmarks
    $(document).ready(function () {
        $('.bookmarks_form').bookmarkForm({
            onSubmit: function (created) {
                if (created) {
                    message.success(gettext("Bookmark created"));
                } else {
                    message.warning(gettext("Bookmark deleted"));
                }
            }
        });
    });
    
    // Scroll to top button
    $(document).ready(function () {
        
        var $scrollButton = $(document.createElement('a'));
        
        $scrollButton.attr({
            'id': 'scrollToTop',
            'href': '#top',
            'name': gettext('Scroll to top')
        });
        
        $('.wrap').append($scrollButton);
        
        if($(window).scrollTop()<300)
            $scrollButton.hide();
            
        $scrollButton.click(function() {
            $("html, body").animate({ scrollTop: 0 }, "slow");
            return false;
        });

        $(window).scroll(function(){
            if($(window).scrollTop()>300) {
                $scrollButton.fadeIn('slow');
            } else {
                $scrollButton.fadeOut('slow');
            }
        });
    });

    
    // List of user's bookmarks to fetch.
    // -------------------------------------------------------------------------
    $(document).ready(function () {
        $('.bookmarks-list-toggle').one('click', function (evt) {
            $.get('/user/my_bookmarks', function (resp) {
                var $list = $('.bookmarks-list');
                resp = JSON.parse(resp);
                if (resp.success) {
                    $(resp.bookmarks).each(function () {
                        var $el = $('<li><a></a></li>'),
                            href = this.target,
                            label = this.label;
                        $el.appendTo($list).find('a')
                            .attr('href', href)
                            .text(label);
                    });
                }
            });
        });
    });
    
    // Submenus for content entries.
    // -------------------------------------------------------------------------
    $('.submenu-toggle').bind('click', function (evt) {
        var $toggle     = $(this),
            $entryTitle = $toggle.parent(),
            $submenu    = $entryTitle.next('.entry-submenu');

        if ($submenu.attr('data-opened') === undefined) {
            $submenu
                .slideDown('fast')
                .attr('data-opened', true)
                .offset({
                    left: $toggle.offset().left - $(this).width(),
                    top:  $toggle.offset().top + $toggle.height()
                });
        } else {
            $submenu
                .slideUp('fast')
                .removeAttr('data-opened');
        }
    });
    
    // Pop-up window with user informations.
    // -------------------------------------------------------------------------
    // Żeby wywołać okienko z informacjami, wystarczy do dowolnego linku 
    // związanego z użytkownikiem dodać parametr data-target równy 'pk' danego
    // użytkownika oraz klasę 'user-window-toggle'.
    //
    (function () {
            // Timeout for popup window to open/close.
        var timeout = null,
            // Helper variable for delay functions.
            trigger = false,
            // Another helper to check if some popup is already opened.
            state   = false;

        // User Backbone model
        // -------------------
        var UserModel = Backbone.Model.extend({});
        // User Backbone view
        // ------------------
        var UserView  = Backbone.View.extend({
            tagName  : 'div',
            className: 'user-popup-window',
            template : _.template($('#user-popup-tpl').html()),
            events: {
                'click .user-popup-close': 'close'
            },
            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
            },
            close: function () {
                this.$el.empty().remove();
            }
        });
        // Backbone user collection
        // ------------------------
        // Holds only one element, which is requested user, but can be easily
        // extended.
        //
        var UserCollection = Backbone.Collection.extend({
                model: UserModel
            });
        // User popup window
        // -----------------
        // Replaces standard Backbone's collection view.
        //
        var UserPopupWindow = function (userdata, toggle) {
            this.model = new UserModel();
            this.collection = new UserCollection([userdata]);
            this.open = function () {
                state = true;
                this.collection.each(function (item) {
                    var view  = new UserView({model:item}),
                        $elem = $(view.render().el);
                    $elem
                        .appendTo('body')
                        .offset({
                            left: toggle.offset().left,
                            top : toggle.offset().top - $elem.height()
                        })
                        .on('mouseout', function () {
                            trigger = true;
                            timeout = setTimeout(function () {
                                if (trigger) {
                                    $elem.empty().remove();
                                }
                            }, 1000);
                        })
                        .on('mouseover', function () {
                            trigger = false;
                            clearTimeout(timeout);
                        });
                });
            };
            this.open();
        };
        // Bind events - open user popup window
        // ------------------------------------
        var openWindow = function ($toggle) {
            var userId = $toggle.attr('data-target');
            $.get('/rest/users/' + userId, function (resp) {
                var win = new UserPopupWindow(resp, $toggle);
            });
        };
        $(document).delegate('.user-window-toggle', 'mouseover', function () {
            var $toggle = $(this);
            trigger = true;
            timeout = setTimeout(function () {
                if (trigger) {
                    openWindow($toggle);
                }
            }, 1000);
        });
        $(document).delegate('.user-window-toggle', 'mouseout', function () {
            trigger = false;
            clearTimeout(timeout);
            if (state) {
                timeout = setTimeout(function () {
                    $('.user-popup-window').empty().remove();
                    state = false;
                }, 1000);
            }
        });
    })();
});