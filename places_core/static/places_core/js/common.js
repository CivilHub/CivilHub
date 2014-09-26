//
// common.js
// =========
//
// Simple common scripts, such as tooltips etc.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/ui/ui',
        'js/utils/utils',
        'js/utils/abuse-report',
        'js/locations/sublocations-popover',
        'bootstrap',
        'js/common/bookmarks'],

function ($, _, Backbone, ui, utils, AbuseWindow, ListView) {
    
    "use strict";
    
    // Zmiana języka
    // -------------
    
    $(document).ready(function () {
        $('#lang-selector > a').popover({
            html: true,
            content: $('#popover-lang-list').html(),
            placement: 'top'
        });
        
        $('#lang-selector > a').on('shown.bs.popover', function () {
            $('body').not('.popover').one('click', function () {
                $('#lang-selector > a').popover('hide');
            });
        });
    });
    
    // Drop-down z sub-lokalizacjami
    // -----------------------------
    
    var dropdown = null; // Aktywne menu
    
    function clearDropdown () {
        if (!_.isNull(dropdown)) {
            dropdown.destroy();
        }
    };
    
    $('.sublocation-menu-toggle').on('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        clearDropdown();
        dropdown = new ListView({
            toggle: $(this),
            id: $(this).attr('data-target')
        });
        $('body').not('.ancestors-menu').one('click', function (e) {
            clearDropdown();
        });
    });
    
    // Abuse reports
    // -------------
    
    if ($('#abuse-modal-tpl').length > 0) {
        (function () {
            var win = null, $link = null;
            $(document).delegate('.report-abuse-link', 'click', function (e) {
                e.preventDefault();
                $link = $(this);
                if (_.isNull(win)) {
                    win = new AbuseWindow({
                        'id': $link.attr('data-id') || 0,
                        'content': $link.attr('data-content') || '',
                        'label': $link.attr('data-label') || ''
                    });
                }
                win.open();
            });
        })();
    };
    
    // Cookie warning message
    // ----------------------
    
    (function($) {
        if(!utils.getCookie('cookie_msg')) {
        
            $('#cookie-msg').prepend('<div class="alert fade in fade out">' + gettext('Cookies help us to deliver our services. By using our services, you agree to our use of cookies') + '.' + '<a class="btn" href="/cookies">' + gettext("Polityka cookies") + '</a><a id="accept-button" class="btn" data-dismiss="alert">OK</a></div>')
                .hide().fadeIn('slow');
            
            $('#accept-button').click(function () {
                var expiration_date = new Date();
                expiration_date.setFullYear(expiration_date.getFullYear() + 1);
                document.cookie = "cookie_msg=true; path=/; domain=.civilhub.org; expires=" + expiration_date.toGMTString();
                $('#cookie-msg').fadeOut('slow', function() {
                    $(this).empty().remove();
                });
            });
        }
    })(jQuery);
    
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
    $('.custom-tooltip-right').tooltip({
        placement: 'right'
    });
    
    // Scroll to top button
    // -------------------------------------------------------------------------
    
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
    
    //
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