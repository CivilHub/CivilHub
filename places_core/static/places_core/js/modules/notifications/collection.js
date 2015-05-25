//
// collection.js
// =============

// Backbone collection for notifications.

define(['backbone',
        'js/modules/notifications/config',
        'js/modules/notifications/model'],

function (Backbone, config, NotifyModel) {

"use strict";

var NotifyCollection = Backbone.Collection.extend({
  model: NotifyModel,
  currentPage: 1,
  url: config.baseUrl + '?page=1',
  parse: function (data) {
    this.hasNext = data.next !== null;
    this.nextUrl = data.next;
    return data.results;
  }
});

return NotifyCollection;

});
