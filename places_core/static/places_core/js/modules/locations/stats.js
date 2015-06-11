//
// stats.js
// ========

// Main module for gettings location's statistics and create
// appropriate charts with Highcharts library support.

require(['jquery',
         'underscore',
         'highcharts3d'],

function ($, _, Highcharts) {

"use strict";

function obj2arr (obj) {
  var data = [];
  for (var prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      data.push([prop, obj[prop]]);
    }
  }
  return data;
}

function fetch (url, data, fn, context) {
  $.get(url, data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

function contentChart (data, $el) {
  var chartOptions = {
    chart: {
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 45
      }
    },
    title: {
      text: data.title
    },
    subtitle: {
      text: data.subtitle
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 45,
        innerSize: 100,
        dataLabels: {
          enabled: true,
          format: '{point.name}'
        }
      }
    },
    tooltip: {
      valueSuffix: '%'
    },
    series: [{
      name: data.name,
      data: data.series
    }]
  };

  $el.highcharts(chartOptions);
}

function summaryChart (data, $el) {
  var chartOptions = {
    chart: {
      type: 'column'
    },
    title: {
      text: data.title
    },
    subtitle: {
      text: data.subtitle
    },
    xAxis: {
      categories: _.map(data.series, function (l) { return l[0]; })
    },
    yAxis: {
      min: 0,
      allowDecimals: false
    },
    credits: {
      enabled: false
    },
    series: [{
      name: data.name,
      colorByPoint: true,
      data: _.map(data.series, function (a) {
        return a[1];
      })
    }]
  };

  console.log(chartOptions);
  $el.highcharts(chartOptions);
}

function timelineChart (data, $el) {
  var startDate = new Date(data.started).getTime();
  var chartOptions = {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: data.title
    },
    xAxis: {
      type: 'datetime',
      labels: {
        format: '{value:%Y. %B %d}',
        rotation: 45
      }
    },
    yAxis: {
      title: {
        text: gettext('Total objects')
      },
      min: 0,
      allowDecimals: false
    },
    series: []
  };

  for (var prop in data.series) {
    if (data.series.hasOwnProperty(prop)) {
      chartOptions.series.push({
        type: 'area',
        pointStart: startDate,
        name: data.labels[prop],
        data: data.series[prop]
      });
    }
  }

  $el.highcharts(chartOptions);
}

function followerChart (data, $el) {
  var startDate = new Date(data.started).getTime();
  var chartOptions = {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: data.title
    },
    subtitle: {
      text: data.subtitle
    },
    xAxis: {
      type: 'datetime',
      labels: {
        format: '{value:%Y. %B %d}',
        rotation: 45
      }
    },
    yAxis: {
      title: {
        text: gettext('Total objects')
      },
      min: 0,
      allowDecimals: false
    },
    series: [{
      type: 'area',
      name: data.name,
      pointInterval: 24 * 3600 * 1000,
      pointStart: new Date(data.started).getTime(),
      data: data.series
    }]
  };

  $el.highcharts(chartOptions);
}

function run () {
  var $contentContainer = $('#content-chart-container');
  var data = JSON.parse($contentContainer.attr('data-series'));
  contentChart(data, $contentContainer);
  var $summaryContainer = $('#summary-chart-container');
  var data = JSON.parse($summaryContainer.attr('data-series'));
  summaryChart(data, $summaryContainer);
  var $timelineContainer = $('#timeline-chart-container');
  var tData = JSON.parse($timelineContainer.attr('data-series'));
  timelineChart(tData, $timelineContainer);
  var $followerContainer = $('#follower-chart-container');
  var fData = JSON.parse($followerContainer.attr('data-series'));
  followerChart(fData, $followerContainer);
}

$(document).ready(run);

});
