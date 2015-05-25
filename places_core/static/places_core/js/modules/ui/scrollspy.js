//
// scrollspy.js
// ============

// A custom wrapper for Bootstrap Scrollspy that creates
// menu automatically based on heading tags found in content.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'bootstrap'],

function ($, _, utils) {

"use strict";

var containerID = 'guide-main-content';
var navbarID = 'guide-main-nav';

function createLinkElement (options) {
  var tpl = _.template('<li><a href="#<%= id %>" class="<%= cls %>"><%= text %></a></li>');
  options = _.extend({ cls: '', text: '', id: '' }, options);
  return $(tpl(options));
}

$(document).ready(function () {
  var $container = $('#' + containerID);
  var $navbar = $('#' + navbarID);
  var opts;
  $container.find('h1,h2,h3,h4,h5,h6').each(function () {
    opts = {
      id: utils.slugify($(this).text()),
      text: $(this).text(),
      cls: 'civil-spy-' + $(this).prop('tagName')
    };
    $(this).attr('id', opts.id);
    $('#' + navbarID + ' > ul').append(createLinkElement(opts));
  });
  $navbar.show('slow');
  $container.scrollspy({ target: '#' + navbarID });
});

});
