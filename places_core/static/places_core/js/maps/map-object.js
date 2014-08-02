//
// map-object.js
// =============
// Prosty widok dla pojedynczego obiektu na mapie.
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var MapObjectView = Backbone.View.extend({
        
        initialize: function () {
            var self = this;
            var latLng = new google.maps.LatLng(
                this.model.get('latitude'),
                this.model.get('longitude')
            );
            this.marker = new google.maps.Marker({
                position: latLng,
                icon: window.STATIC_URL + '/icons/marker-' + 
                    window.CONTENT_TYPES[self.model.get('content_type')].model 
                    + '.png'
            });
            google.maps.event.addListener(this.marker, 'click', function () {
                console.log(self.model.get('latitude'));
                self.getData();
            });
        },
        
        getData: function () {
            $.get('/api-maps/objects/'+this.model.get('id')+'/', function (resp) {
                console.log(resp);
            });
        }
    });
    
    return MapObjectView;
});