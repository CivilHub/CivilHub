//
// actionCollection.js
// ===================
//
// Manage user actions.

define(['backbone',
        'js/modules/actstream/actions/actionModel'],

function (Backbone, ActionModel) {

    "use strict";
    
    var ActionCollection = Backbone.Collection.extend({
        
        model: ActionModel
    });
    
    return ActionCollection;
});