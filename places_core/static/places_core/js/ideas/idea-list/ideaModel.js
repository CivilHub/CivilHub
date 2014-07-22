//
// ideaModel.js
// ============
// Basic model for idea list.
define(['backbone', 'moment'],

function (Backbone) {
    "use strict";
    
    var IdeaModel = Backbone.Model.extend({
        initialize: function (params) {
            if (params) {
                this.set('date_created', moment(params.date_created).fromNow());
            }
        }
    });
    
    return IdeaModel;
});