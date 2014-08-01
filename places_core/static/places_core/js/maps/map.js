//
// map.js
// ======
// Główny widok mapy.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/maps/map-collection',
        'js/maps/map-object'],

function ($, _, Backbone, MapCollection, MapObject) {
    
    "use strict";
    
    var CivilMap = Backbone.View.extend({
        
        initialize: function () {
            this.map = new google.maps.Map(document.getElementById('map'));
        }
    });
    
    return CivilMap;
});