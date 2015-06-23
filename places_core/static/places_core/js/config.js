//
// config.js
// =========
//
// Configuration for entry files for the files that are in the js/src catalog.
// A separate configuration for builds is located in config.json.
// Unfortunately, 'path' and 'shim' have to be repeated therefore if we add
// something in one file, we have to also include it in the other.

require.config({

  baseUrl: CivilApp.staticURL,

  urlArgs: "bust=" + (new Date()).getTime(),

  waitSeconds: 0,

  "paths": {
    "masonry": "includes/masonry/masonry.pkgd.min",
    "ga": "//www.google-analytics.com/analytics",
    "text": "includes/require/text",
    "jquery": "includes/jquery/jquery",
    "jqueryui": "includes/jquery-ui/jquery-ui",
    "jpaginate": "includes/jquery/jquery.paginate",
    "bootstrap": "includes/bootstrap/bootstrap",
    "bootbox": "includes/bootstrap/bootbox",
    "underscore": "includes/underscore/underscore",
    "backbone": "includes/backbone/backbone",
    "paginator": "includes/backbone/backbone.paginator",
    "moment": "includes/momentjs/moment",
    "tagsinput": "includes/jquery/jquery.tagsinput",
    "bootstrap-switch" : "includes/bootstrap/bootstrap-switch",
    "redactor": "includes/redactor/redactor",
    "dropzone": "includes/dropzone/dropzone",
    "leaflet": "includes/leaflet/leaflet",
    "fullpagejs": "includes/fullpagejs/jquery.fullPage",
    "color": "includes/jquery/jquery.color",
    "Jcrop": "includes/jquery/jquery.Jcrop",
    "file-input": "includes/bootstrap/bootstrap.file-input",
    "vector": "includes/vectormap/jquery-jvectormap-1.2.2.min",
    "worldmap": "includes/vectormap/jquery-jvectormap-world-mill-en",
    "tubular": "includes/tubular/jquery.tubular.1.0",
    "tour": "includes/tour/bootstrap-tour",
    "hammer": "includes/mapplic/hammer",
    "jeasing": "includes/mapplic/jquery.easing",
    "mapplic": "includes/mapplic/mapplic",
    "jmousewheel": "includes/mapplic/jquery.mousewheel",
    "CUri": "includes/curi",
    "lightbox": "includes/lightbox",
    "facebook": "//connect.facebook.net/en_US/sdk",
    "highcharts": "includes/highcharts/js/highcharts",
    "highchartsTheme": "includes/highcharts/js/themes/sand-signika",
    "highcharts3d": "includes/highcharts/js/highcharts-3d"
  },

  "shim": {

    "masonry": {
      "deps": ["jquery"],
      "exports": "Masonry"
    },

    "highcharts": {
      "deps": ["jquery"],
      "exports": "Highcharts"
    },

    "highchartsTheme": {
      "deps": ["highcharts"],
      "exports": "Highcharts"
    },

    "highcharts3d": {
      "deps": ["highchartsTheme"],
      "exports": "Highcharts"
    },

    "leaflet": {
      "exports": "L"
    },

    "facebook": {
      "exports": "FB"
    },

    "tour": {
      "deps": ["bootstrap"]
    },

    "tubular": {
      "deps": ["jquery"]
    },

    "jqueryui": {
      "deps": ["jquery"]
    },

    "tagsinput": {
      "deps": ["jqueryui"]
    },

    "jpaginate": {
      "deps": ["jquery"]
    },

    "underscore": {
      "deps": ["jquery"],
      "exports": "_"
    },

    "backbone": {
      "deps": ["underscore"],
      "exports": "Backbone"
    },

    "bootstrap": {
      "deps": ["jquery"]
    },

    "bootbox": {
      "deps": ["bootstrap"],
      "exports": "bootbox"
    },

    "bootstrap-switch": {
      "deps": ["bootstrap"]
    },

    "fullpagejs": {
      "deps": ["jquery"]
    },

    "color": {
      "deps": ["jquery"]
    },

    "Jcrop": {
      "deps": ["color"]
    },

    "file-input": {
      "deps": ["bootstrap"]
    },

    "vector": {
      "deps": ["jquery"]
    },

    "worldmap": {
      "deps": ["vector"]
    },

    "hammer": {
      "deps": ["jquery"]
    },

    "jeasing": {
      "deps": ["jquery"]
    },

    "jmousewheel": {
      "deps": ["jquery"]
    },

    "mapplic": {
      "deps": ["jquery"]
    }
  }
});

// Here you can place scripts and configurations that
// will load before any other script on the site.

require(['moment',
         'backbone',
         'js/modules/utils/utils',
         'ga'],

function (moment, Backbone, utils) {

  "use strict";

  // Set global locales for moment.js

  moment.locale(CivilApp.language);

  // Global Backbone overrides

  Backbone._sync = Backbone.sync;

  Backbone.sync = function (method, model, options) {
    if (method == 'create' || method == 'update' || method == 'delete') {
      $.ajaxSetup({
        headers: { 'X-CSRFToken': utils.getCookie('csrftoken') }
      });
    }
    return Backbone._sync(method, model, options);
  };

  // Google Analytics - should be moved to separate file

  window.ga('create', 'UA-51512403-1', 'auto');
  window.ga('require', 'linkid', 'linkid.js');
  window.ga('send', 'pageview');

  window.CivilApp.gaEvents = {
    voteIdea: function (vote) {
      switch (vote) {
        case 1: window.ga('send', 'event', 'vote', 'click', 'vote-yes'); break;
        case 2: window.ga('send', 'event', 'vote', 'click', 'vote-no'); break;
        case 3: window.ga('send', 'event', 'vote', 'click', 'revoke'); break;
      }
    }
  };
});
