//
// minimap.js
// ==========
//
// Display minimap for different content types. Minimap shows all map pointers
// related to selected content item and allow registered user to delete them.
// Note that Google API key is already attached to requirements.

define(['jquery',
        'underscore',
        'js/ui/ui',
        'bootstrap',
        'async!//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false'],

function ($, _, ui) {
    
    "use strict";
    
    // Usuwanie markerów
    // -------------------------------------------------------------------------
    
    function deleteMarker (marker) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            type: 'DELETE',
            url: '/api-maps/pointers/'+marker.mapObject.pk,
            success: function (resp) {
                ui.message.success(gettext('Marker deleted'));
                marker.setVisible(false);
            },
            error: function (err) {
                console.log(err);
            }
        });
    };
    
    
    // Minimapa
    // -------------------------------------------------------------------------
    
    var Minimap = function (markers) {
        this.markers = markers || [];
        this.center = markers[0] || {lat: 0, lng: 0};
        if (this.markers.length > 0) {
            this.initialize();
        }
    };
    
    Minimap.prototype.initialize = function () {
        this.template = _.template($('#minimap-tpl').html());
        this.$el = $(document.createElement('div'));
        this.$el.html(this.template({}));
        this.$el.addClass('modal fade');
        this.$el.modal({show:false});
        this.$el.on('shown.bs.modal', function (e) {
            this.createMap();
        }.bind(this));
    };
    
    Minimap.prototype.createMap = function () {
        var el = document.getElementById('minimap');
        var ct = this.center;
        var mapOptions = {
                zoom: 6,
                center: new google.maps.LatLng(
                    parseInt(ct.lat, 10),
                    parseInt(ct.lng, 10)),
                width: 800,
                height: 600
            };
        this.map = new google.maps.Map(el, mapOptions);
        _.each(this.markers, function (item) {
            this.addMarker(item);
        }, this);
    };
    
    Minimap.prototype.addMarker = function (item) {
        var m = new google.maps.Marker(),
            pos = new google.maps.LatLng(
                parseInt(item.lat, 10), parseInt(item.lng, 10)
            );
        m.setMap(this.map);
        m.setPosition(pos);
        m.mapObject = item;
        google.maps.event.addListener(m, 'click', function() {
            ui.confirmWindow(deleteMarker, null, [m]);
        });
    };
    
    Minimap.prototype.open = function () {
        this.$el.modal('show');
    };
    
    Minimap.prototype.close = function () {
        this.$el.modal('hide');
    };
    
    return Minimap;
    
});