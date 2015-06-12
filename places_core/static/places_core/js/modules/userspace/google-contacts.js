//
// google-contacts.js
// ==================

// The application allows to send invites on Gmail contact addresses list
// of the authenticated user

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/utils',
        'js/modules/ui/ui',
        'bootstrap',
        'includes/google/client'],

function ($, _, Bootstrap, utils, ui) {

"use strict";

var ContactModel = Backbone.Model.extend({});

var ContactView = Backbone.View.extend({

  tagName: 'li',

  className: 'contact-entry',

  template: _.template($('#google-contacts-entry-tpl').html()),

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  }
});

var ContactsCollection = Backbone.Collection.extend({

  model: ContactModel
});

var ContactListView = Backbone.View.extend({

  el: '#contact-list',

  initialize: function (options) {
    this.$modal = this.$el.parents('.modal').first();
    this.$form = this.$modal.find('form:first');
    this.$submit = this.$modal.find('.submit-btn:first');
    this.collection = new ContactsCollection(options.contacts);
    this.render();

    this.$form.on('submit', function (e) {
      e.preventDefault();
      this.submit();
      this.close();
    }.bind(this));

    this.$submit.on('click', function (e) {
      e.preventDefault();
      this.$form.trigger('submit');
    }.bind(this));

    $('#check-all-button').on('click', function (e) {
      this.toggleAll();
    }.bind(this));
  },

  render: function () {
    this.collection.each(function (item) {
      this.renderItem(item);
    }, this);
  },

  renderItem: function (item) {
    var contact = new ContactView({
      model: item
    });
    $(contact.render().el).appendTo(this.$el);
  },

  submit: function () {

    var addresses = [];

    this.$form.find('[type=checkbox]').each(function () {
      if ($(this).is(':checked')) {
        addresses.push($(this).val());
      }
    });

    $.post('/civmail/', {
      emails: addresses.join(','),
      link: 'https://civilhub.org/',
      name: 'Civilhub.org',
      csrfmiddlewaretoken: utils.getCookie('csrftoken')
    }, function (resp) {
      ui.message.success(gettext("All messages sent successfully"));
    });
  },

  toggleAll: function () {
    this.$form.find('[type=checkbox]').each(function () {
      $(this).trigger('click');
    });
  },

  open: function () {
    this.$modal.modal('show');
  },

  close: function () {
    this.$modal.modal('hide');
  }
});

return ContactListView;

});
