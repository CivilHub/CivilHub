/**
 * collection.js
 * =============
 *
 * Wrapper for ``Backbone.Collection`` adjusted to work
 * with map for voting.
 */

define(['backbone',
        'js/modules/mapvotes/common/model'],

function (Backbone, MarkerModel) {

"use strict";

var MarkerCollection = Backbone.Collection.extend({
    model: MarkerModel
});

return MarkerCollection;

});

