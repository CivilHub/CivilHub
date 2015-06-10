//
// chartmaker.js
// =============

// Creates proper charts for poll results.

require(['jquery',
         'underscore',
         'highcharts3d'],

function ($, _, Highcharts) {

"use strict";

// Base service URL to fetch answers.

var baseurl = "/api-polls/answers/";

// Similar to the above - url to fetch timeline data.

var timeUrl = '/api-polls/timeline/';

// Another url, this time for visit counter data

var counterUrl = '/api-hitcounter/graph/';

// Custom wrapper to perform GET request and pass context to callback.

function fetch (url, data, fn, context) {
  $.get(url, data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

// Simplified function that converts response object to array.

function obj2arr (obj) {
  var data = [];
  for (var prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      data.push([prop, obj[prop]]);
    }
  }
  return data;
}

// Creates simple chart for polls with 'multiple' option enabled.

function drawSimpleChart (response) {
  $('#chart-container').highcharts({
    chart: {
      type: 'bar'
    },
    title: {
      text: response.title
    },
    xAxis: {
      categories: _.map(obj2arr(response.answers), function (a) {
        return a[0];
      }),
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      allowDecimals: false,
      title: {
        text: 'Answer count'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      valueSuffix: ' answers'
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
        }
      }
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 100,
      floating: true,
      borderWidth: 1,
      backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
      shadow: true
    },
    credits: {
      enabled: false
    },
    series: [{
      name: 'Total Answers',
      data: _.map(obj2arr(response.answers), function (a) {
        return a[1];
      })
    }]
  });
}

// This function creates chart for polls that allows only one answer.

function drawPieChart (response) {
  $('#chart-container').highcharts({
    chart: {
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 45,
        beta: 0
      }
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        innerSize: 100,
        dataLabels: {
          enabled: true,
          format: '{point.name}'
        }
      }
    },
    title: {
      text: response.title
    },
    tooltip: {
      valueSuffix: '%'
    },
    series: [{
      type: 'pie',
      name: 'Total Answers',
      data: obj2arr(response.answers)
    }]
  });
}

// Creates timeline chart containing answer map in relation to date.

function drawTimelineChart (data) {
  var startDate = new Date(data.date_created).getTime();
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
        text: 'Total votes'
      },
      min: 0,
      allowDecimals: false
    },
    series: []
  };

  _.each(data.labels, function (label) {
    chartOptions.series.push({
      type: 'line',
      name: label.label,
      pointStart: startDate,
      data: data.answers[label.id]
    });
  });

  $('#chart-container').highcharts(chartOptions);
}

// Draw chart with visit counter statictics for main poll's page

function drawVisitChart (data) {
  var chartOptions = {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: data.title
    },
    subtitle: {
      text: document.ontouchstart === undefined ?
        gettext('Click and drag in the plot area to zoom in') :
        gettext('Pinch the chart to zoom in')
    },
    xAxis: {
      type: 'datetime',
      minRange: 14 * 24 * 3600000 // fourteen days
    },
    yAxis: {
      title: {
        text: gettext('Total visits')
      },
      min: 0,
      allowDecimals: false
    },
    legend: {
      enabled: false
    },
    plotOptions: {
      area: {
        fillColor: {
          linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
          stops: [
            [0, Highcharts.getOptions().colors[0]],
            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
          ]
        },
        marker: {
          radius: 2
        },
        lineWidth: 1,
        states: {
          hover: {
            lineWidth: 1
          }
        },
        threshold: null
      }
    },
    series: [{
      type: 'area',
      name: gettext('Visits'),
      pointInterval: 24 * 3600 * 1000,
      pointStart: new Date(data.start_time).getTime(),
      data: data.results
    }]
  };

  $('#chart-container').highcharts(chartOptions);
}

// Simple wrapper that initializes first graph.

function initChart (pk) {
  fetch(baseurl, { pk: pk }, function (response) {
    if (response.multiple) {
      drawSimpleChart(response);
    } else {
      drawPieChart(response);
    }
  });
}

// Timeline graph presenting different data output.

function timeChart (pk) {
  fetch(timeUrl, { pk: pk }, function (response) {
    drawTimelineChart(response);
  });
}

// Timeline graph presenting different visit statistics.

function visitChart(pk, ct) {
  fetch(counterUrl, { pk: pk, ct: ct }, function (response) {
    drawVisitChart(response);
  });
}

// Run everything!

$(document).ready(function () {
  var currentID = parseInt($('#chart-container').attr('data-target'), 10);
  var currentCT = parseInt($('#chart-container').attr('data-content'), 10);
  initChart(currentID);
  $('#chart-switch').on('change', function () {
    switch ($(this).val()) {
      case "1": initChart(currentID); break;
      case "2": timeChart(currentID); break;
      case "3": visitChart(currentID, currentCT); break;
    }
  });
});

});
