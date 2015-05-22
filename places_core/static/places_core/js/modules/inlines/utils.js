//
// utils.js
// ========

// Multi-purpose functions to use in entire application.

define(['jquery',
        'underscore',
        'js/modules/utils/utils'],

function ($, _, utils, CommentModel) {

"use strict";

var cUtils = {};

// This is shortcut to create new comment instance.
//
// @param { obj } Comment data (see in list.js how it's implemented)
// @param { Backbone.Collection } Collection to work on
// @param { function } Callback function
// @param { context } Parent object (help to pass 'this')

cUtils.createComment = function (comment, collection, callback, context) {
  var data = {
    csrfmiddlewaretoken: utils.getCookie('csrftoken'),
    comment: comment.comment,
    object_pk: comment.pk,
    content_type: comment.ct,
    submit_date: moment().format(),
    site: 1
  };
  if (!_.isUndefined(comment.parent)) {
    data.parent = comment.parent;
  }
  $.post('/api-comments/list/', data, function (response) {
    $.get('/api-comments/list/' + response.id + '/',
      function (data) {
        if (_.isFunction(callback)) {
          callback.call(context, data);
        }
      }
    );
  });
};

return cUtils;

});
