//
// map-collection.js
// =================
// Obsługa kolekcji znaczników do mapy.
define(['jquery',
        'underscore',
        'backbone',
        'js/maps/map-model'],

function ($, _, Backbone, MapModel) {
    
    "use strict";
    
    var MapCollection = Backbone.Collection.extend({
        model: MapModel
    });
    
    return MapCollection;
});