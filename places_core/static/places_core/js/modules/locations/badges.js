//
// badges.js
// =========
//
define(['jquery',
        'underscore',
        'backbone',
        'bootstrap'],

function ($, _, Backbone) {
    "use strict";
    // Prepare DOM elements and common variables/constants
var sel    = null, // Placeholder for entire badge selector form.
    $modal = $('#select-badge-form'),
    $sBtn  = $modal.find('.submit-btn'),
    URL    = '/rest/badges/';
    
// Prepare modal widow
$modal.modal({show: false});

// Basic Badge model.
// ------------------

// Single badge element.
var BadgeModel = Backbone.Model.extend({});

// Badge View
// ----------

// Show single badge in modal window.
var BadgeView = Backbone.View.extend({
    // Customize badge element
    className: 'badge-entry row',
    // Process template (from html file)
    template: _.template($('#badge-tpl').html()),
    // Track selected elements
    selected: false,
    // Display badge
    render: function () {
        this.$el.html(this.template($.extend(this.model.toJSON())));
        return this;
    },
    // Highlight clicked badge and mark it as selected
    activate: function () {
        this.$el.addClass('badge-selected');
        this.selected = true;
    },
    // Unselect given badge
    deactivate: function () {
        this.$el.removeClass('badge-selected');
        this.selected = false;
    }
});

// Badge collection
// ----------------

// Manage entire badge list.
var BadgeCollection =  Backbone.Collection.extend({
    model: BadgeModel
});

// Badge selector
// --------------

// Modal window form that allow users to choose one
// of existing badges and give it to selected location
// follower.
var BadgeSelector = function ($el) {
    var that = this;
        // Modal window DOM element
        that.window = $el;
        // Element for backbone collection
        that.elem   = $el.find('.modal-body');
        // Simple - submit button
        that.submit = $el.find('.submit-btn');
        // Target user to which you want to give badge
        that.target = null;
        // Empty object to hold selected bagde.
        that.selection  = {};
        // Connect models to views
        that.badgeViews = {};
        
        // User selection functions
        // ------------------------
        
        // Check if user selected any badge and send PUT request if so.
        that.submit.bind('click', function (evt) {
            evt.preventDefault();
            if (!_.isNull(that.target) && !_.isEmpty(that.selection)) {
                var formData = {
                    id: that.selection.get('id'),
                    user: that.target
                }
                // save
                that.save(formData);
                return true;
            }
            return false;
        });
        // Save selection - core function
        // @param data {
        //          id  : badge object ID
        //          user: target user pk
        //        }
        that.save = function (data) {
            sendAjaxRequest('PUT', URL, {
                data: data,
                success: function (resp) {
                    console.log(resp);
                    that.close();
                    if (resp.success) {
                        display_alert(resp.message, 'success');
                    } else {
                        display_alert(resp.message, 'danger');
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        };
        
        // Manipulate modal window
        // -----------------------
        
        // Open modal window and set target user ID.
        that.open = function (userId) {
            that.window.modal('show');
            that.target = userId;
        };
        // Hide modal window.
        that.close = function () {
            that.window.modal('hide');
        };
        
        // Render DOM elements
        // -------------------
        
        // Render single badge entry.
        that.renderBadge = function (item) {
            var ItemView = new BadgeView({
                model: item
            });
            var $element = $(ItemView.render().el);
            $element.prependTo(that.elem);
            // Link views with models by their ID
            that.badgeViews[item.get('id')] = ItemView;
            $element.on('click', function () {
                that.selectBadge(item.get('id'));
            });
        };
        // User selection - highlight selected badge
        that.selectBadge = function (itemId) {
            var key, v;
            for (key in that.badgeViews) {
                v = that.badgeViews[key];
                if (key == itemId) { // "==" is important
                    v.activate();
                    that.selection = v.model;
                } else {
                    v.deactivate();
                }
            }
        };
        // Render entire collection.
        that.render = function () {
            that.badges.each(function (item) {
                that.renderBadge(item);
            });
        };
        
        // Initialize selector
        // -------------------
        
        // Create backbone badges collection.
        $.get(URL, function (badges) {
            that.badges = new BadgeCollection(badges);
            that.render();
        });
        // Connect to DOM via 'data' jQuery function
        that.window.data('BadgeSelector', that);
    }

    // Create new badge selector form.
    // -------------------------------
    sel = new BadgeSelector($modal);

    // Run scripts.
    // ------------

    $('.moderator-badge-add').bind('click', function (evt) {
        evt.preventDefault();
        sel.open($(this).attr('data-target'));
    });
    
    //
    // Show only five first locations in follower entry and give users link
    // to hide/show rest of them.
    // -------------------------------------------------------------------------
    //
    $('.follows-places').each(function () {
        // If list is too short, simply return.
        if ($(this).find('li').length <= 5) {
            return true;
        }
        // Prepare DOM elements.
        var $entry  = $(this),
            $links  = $entry.children('li'),
            $toggle = $(document.createElement('a')),
            $hide   = $(document.createElement('a')),
            hidden  = [];
        // For each item, hide it if necessary.
        $links.each(function (idx, el) {
            if (idx > 4) {
                $(el).hide();
                hidden.push($(el));
            }
        });
        // Show hidden links.
        $toggle.appendTo($entry)
            .text('{% trans "Show more" %}')
            .attr('href', '#')
            .on('click', function (evt) {
                evt.preventDefault();
                $(hidden).each(function () {
                    $(this).show('fast');
                });
                $toggle.fadeOut('fast');
                $hide.fadeIn('fast');
            });
        // Hide hidden links.
        $hide.appendTo($entry)
            .hide()
            .text('{% trans "Hide" %}')
            .attr('href', '#')
            .on('click', function (evt) {
                evt.preventDefault();
                $(hidden).each(function () {
                    $(this).hide('fast');
                });
                $hide.fadeOut('fast');
                $toggle.fadeIn('fast');
            });
    });
});