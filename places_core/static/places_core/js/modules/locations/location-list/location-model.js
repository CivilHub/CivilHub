//
// location-model.js
// =================

define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var LocationModel = Backbone.Model.extend({
        defaults: {
            id: 0,
            name: 'Unknown',
            slug: 'Unknown'
        }
    });
    
    return LocationModel;
});