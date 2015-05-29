//
// facebook.js
// ===========

// Custom wrapper function to use along with FB API.

define(['underscore',
        'facebook',
        'js/modules/utils/utils'],

function (_, FB, utils) {

"use strict";

// External function to fetch initiali FB data and pass 'this' object as needed.
//
// @param Function Callback to trigger on successfull check.
// @param Object 'this' value to pass into callback function.

function getStatus (fn, context) {
  FB.getLoginStatus(function (response) {
    if (response.status === 'connected') {
      if (_.isFunction(fn)) {
        fn.call(context, response);
      }
    }
  });
}

// Perform request to Graph API. As above, this allows us to bind response.
//
// @param SAtring API path (see Graph API reference for details)
// @param Object Plain object with data to send.
// @param Function Callback to trigger on success
// @param Object "This" value to pass into callback functions

function apiRequest (path, data, success, context) {
  FB.api(path, data, function (response) {
    if (_.isFunction(success)) {
      success.call(context, response);
    }
  });
}

// -----------------------------------------------------------------------------
//
// Basic wrapper object. This object wraps different FB API functions, so that
// most of it's methods takes callback and context arguments as parameters.
// This allows us to pass any callback function bound to any given object and
// talk with Graph API itself by this common interface.
//
// -----------------------------------------------------------------------------

function CFBConnector () {
  var _this = this;
  FB.init({
    appId: CivilApp.fbClientToken,
    version: 'v2.3'
  });
  getStatus(this.initialize, this);
}

// Append access_token to data object for any API request.
//
// @param Object Plain object with data to send. Depends on function.

CFBConnector.prototype.setData = function (data) {
  return _.extend({ access_token: this.token }, data);
};

// Set initial data returned by FB auth object
//
// @param Object Plain object with FB server response.

CFBConnector.prototype.initialize = function (response) {
  this.token = response.authResponse.accessToken;
  this.user = response.authResponse.userID;
  this.expires = response.authResponse.expiresIn;
};

// Get list of user's friends that also uses our application.

CFBConnector.prototype.friendList = function (fn, context) {
  var data = this.setData({ fields: 'id' });
  return apiRequest('/me/friends', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
};

CFBConnector.prototype.checkFriends = function () {
  this.friendList(function (response) {
    var friends = _.map(response.data, function (f) {
      return f.id;
    });
    var data = {
      csrfmiddlewaretoken: utils.getCookie('csrftoken'),
      friends: friends.join(',')
    };
    console.log(data);
    $.post('/user/facebook-friends/', data, function (r) {
      console.log(r);
    });
  }, this);
};

// Returns total number of friends. As always, you have to pass
// callback function and integer will be passed to this function.

CFBConnector.prototype.countFriends = function (fn, context) {
  var data = this.setData({ fields: 'id' });
  return apiRequest('/me/friends', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response.summary.total_count);
    }
  });
};

// Test function - get current user's last name.

CFBConnector.prototype.getLastName = function (fn, context) {
  var data = this.setData({ fields: 'last_name' });
  return apiRequest('/me', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
};

return CFBConnector;

});
