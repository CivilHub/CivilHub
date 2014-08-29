//
// map-pointer-view.js
// ===================
// Widok dla wszystkich markerów na mapie poza lokacjami.
define(['jquery',
        'underscore',
        'backbone',
        'js/maps/map-object'],

function ($, _, Backbone, MapObjectView) {
    
    "use strict";
    
    var MapPointerView = MapObjectView.extend({
        
        getData: function () {
            
            var self = this,
                ct = this.model.get('content_type'),
                url = '/api-maps/objects/?ct='+ct+
                      '&pk='+this.model.get('object_pk'),
                ct = this.model.get('content_type');
                                 
            $.get(url, function (m) {
                
                try {
                    m = m[0].content_object;
                } catch (e) {
                    console.log(e);
                    alert("Object not found");
                    return false;
                }
                
                var contentString = window.mapDialogTpl({
                        url: m.url,
                        type: m.type,
                        title: m.title,
                        desc: m.desc,
                        date: m.date,
                        img: m.img,
                        user: m.user,
                        profile: m.profile,
                        content_type: ct
                    });
                    
                self.showInfo(contentString, self.map, self.marker);
            });
        }
    });
    
    return MapPointerView;
});