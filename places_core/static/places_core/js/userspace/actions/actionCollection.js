//
// actionCollection.js
// ===================
//
// Manage user actions.
//
define(['backbone',
        'js/userspace/actions/actionModel'],

function (Backbone, ActionModel) {
    "use strict";
    
    var ActionCollection = Backbone.Collection.extend({
        
        model: ActionModel,
        
        url: '/rest/my_actions/'
    });
    
    return ActionCollection;
});