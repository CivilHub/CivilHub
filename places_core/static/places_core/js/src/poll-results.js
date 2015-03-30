//
// poll-results.js
// ===============
// 
// Single poll results review.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'dateAxisRenderer',
           'canvasTextRenderer',
           'canvasAxisTickRenderer',
           'categoryAxisRenderer',
           'barRenderer',
           'js/modules/ui/ui',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter'],

  function ($, ui) {
      
    "use strict";
    
    var plot1 = $.jqplot('chartdiv', [window.POLLS.asets], {
      title: window.POLLS.title,
      animate: true,
      series:[{renderer:$.jqplot.BarRenderer}],
      axesDefaults: {
        tickRenderer: $.jqplot.CanvasAxisTickRenderer,
        tickOptions: {
          angle: -30,
          fontSize: '10pt'
        }
      },
      axes: {
        xaxis: {
          renderer: $.jqplot.CategoryAxisRenderer
        }
      }
    });
    
    $(document).trigger('load');
      
  });
});