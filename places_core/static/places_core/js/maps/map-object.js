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
                    + '.png',
                content_type: self.model.get('content_type')
            });
            google.maps.event.addListener(this.marker, 'click', function () {
                self.getData();
            });
        },
        
        getData: function () {
            var self = this,
                isLocation = window.CONTENT_TYPES[self.model.get('content_type')].model === 'location',
                ct = self.model.get('content_type'),
                url = isLocation ? '/api-locations/locations/' + this.model.get('id') + '/'
                                 : '/api-maps/objects/?ct='+ct+'&pk='+this.model.get('object_pk');
            $.get(url, function (m) {
                m = isLocation ? m : m[0].content_object;
                var contentString;
                if (isLocation) {
                    contentString = window.locDialogTpl({
                        name: m.name,
                        img: m.image,
                        slug: m.slug
                    });
                } else {
                    contentString = window.mapDialogTpl({
                        url: m.url,
                        type: m.type,
                        title: m.title,
                        desc: m.desc,
                        date: m.date,
                        img: m.img,
                        user: m.user,
                        profile: m.profile
                    });
                }
                
                var infoWindow = new google.maps.InfoWindow({
                    content: contentString
                });
                
                infoWindow.open(self.map, self.marker);
                
                $(document).one('click', function (e) {
                    infoWindow.close();
                });
            });
        }
    });
    
    return MapObjectView;
});