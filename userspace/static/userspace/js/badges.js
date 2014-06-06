(function ($) {
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
    },
    // Unselect given badge
    deactivate: function () {
        this.$el.removeClass('badge-selected');
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
    // Check if user selected any badge and send POST request if so.
    that.submit.bind('click', function () {
        if (!_.isNull(that.target) && !_.isEmpty(that.selection)) {
            var formData = {
                id: that.selection.get('id'),
                user: that.target
            }
            that.save(formData, that.close);
        }
    });
    that.save = function (data, callback) {
        sendAjaxRequest('PUT', URL, {
            data: data,
            success: function (resp) {
                console.log(resp);
                callback();
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
    // Open modal window and set target user ID.
    that.open = function (userId) {
        that.window.modal('show');
        that.target = userId;
    };
    // Hide modal window.
    that.close = function () {
        that.window.modal('hide');
    };
    // Render single badge entry.
    that.renderBadge = function (item) {
        var ItemView = new BadgeView({
            model: item
        });
        var $element = $(ItemView.render().el);
        $element.prependTo(that.elem);
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
            if (key == itemId) {
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

$('.moderator-badge-add').bind('click', function () {
    sel.open($(this).attr('data-target'));
});
    
})(jQuery);