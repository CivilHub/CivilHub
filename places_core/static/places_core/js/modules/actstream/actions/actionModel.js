//
// actionModel.js
// ==============
//
// Base model for all actions.
//
define(['backbone'],

function (Backbone) {
    
    "use strict";
    
    var ActionModel = Backbone.Model.extend({
        defaults: {
            'description': ''
        }
    });
    
    return ActionModel;
});