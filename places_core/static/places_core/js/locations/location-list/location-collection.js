//
// location-collection.js
// ======================

define(['jquery',
        'underscore',
        'backbone',
        'js/locations/location-list/location-model'],

function ($, _, Backbone, LocationModel) {
    
    "use strict";
    
    var LocationCollection = Backbone.Collection.extend({
        
        model: LocationModel
    });
    
    return LocationCollection;
});