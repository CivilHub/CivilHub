//
// bouncy-menu.js
// ==============

// A script that allows us to automatically fill in the menu
// base on te list of lcations currently followed by the user

define(['jquery',
        'underscore'],

function ($, _, utils) {

"use strict";

var url = '/api-userspace/locations/';
var tpl = _.template('<option value="<%= slug %>"><%= name %></option>');

// A small helper that creates an url
//
// @param { String } The slug of a chosen location
// @param { String } A url elemnt that points to this type of content

function createUrl (slug, content) {
  return ("/{slug}/{content}/create/")
  .replace(/{slug}/g, slug)
  .replace(/{content}/g, content);
}

// We change the active location

function switchOptions (e) {
  $('.bouncy-option').each(function () {
    $(this).attr('href', createUrl(
    $(e.currentTarget).val(),
    $(this).attr('data-content'))
    );
  });
}

// Creates a menu automatically
//
// @param { jQuery.DomElement } Element select in jQuery

function createMenu ($select) {
  $.get(url, function (locations) {
    var slug = $select.attr('data-location');
    var $option;

    // If we are in an active location, we set it to the chosen one,
    // else we take the first from the chosen list
    if (_.isUndefined(slug) && locations.length) {
      slug = locations[0].slug;
    }

    _.each(locations, function (location) {

      // We are in the subpage of the location and a location is chosen.
      // In this case, the option is already available therefore we don't
      // create a new one
      if (location.slug === $select.attr('data-location')) {
        return true;
      }

      // We create all other options from the followed locations
      $option = $(tpl(location));
      if (location.slug === slug) {
        $option.attr('selected', 'selected');
      }
      $select.append($option);
    });

    // We fill in the url-s in the links
    $('.bouncy-option').each(function () {
      this.href = createUrl(slug, $(this).attr('data-content'));
    });
    $select.on('change', switchOptions);

    // We make sure that we have something to show
    if ($select.find('option').length) {
      $select.show();
    }
  });
}

// A widget that complements the bouncy-menu. It allows
// us to dynamically substitute the links in options depending
// on the current location
$.fn.bouncyMenu = function () {
  return $(this).each(function () {
    createMenu($(this));
  });
};

return $.fn;

});
