//
// media-uploader.js
// =================
//
// A modal window with user gallery service. Allows for uploading and deletion
// of images in the user gallery that has an active sesion. In order to work
// it needs a template from /templates/gallery/media-uploader.html file.
// -----------------------------------------------------------------------------

define(['jquery',
        'underscore',
        'backbone',
        'dropzone'],

function ($, _, Backbone, Dropzone) {
    
    "use strict";
    
    // Allows to evade 'dropzone already attached' error
    Dropzone.autodiscover = false;
    
    //
    // MediaModel
    // ==========
    
    var MediaModel = Backbone.Model.extend({
        // We add a slash at the end of the address due to Django security
        url: function() {
            var original_url = Backbone.Model.prototype.url.call(this),
                parsed_url = original_url + (original_url.charAt(original_url.length - 1) == '/' ? '' : '/');

            return parsed_url;
        } 
    });
    
    //
    // MediaCollection
    // ===============
    
    var MediaCollection = Backbone.Collection.extend({
        
        model: MediaModel,
        
        url: '/api-gallery/usermedia/',
        
        initialize: function () {
            // Necessary due to Django csrf protection
            $.ajaxSetup({
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            });
        }
    });
    
    //
    // MediaItem
    // =========
    // A view for a single element collection (images)
    
    var MediaItem = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'media-entry',

        template:  _.template($('#media-item-tpl').html()),

        events: {
            'click .delete-item-button': 'remove'
        },
        
        isActive: false, // We mark the element as active/highlighted

        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            // Highlight the element selected by the user
            this.$el.on('click', function (e) {
                e.preventDefault();
                // We refer to the view of the whole window, we select the active
                // element and we unselect all the other
                this.parentView.markSelected(this);
            }.bind(this));
            return this;
        },
        
        activate: function () {
            this.$el.addClass('active');
            this.isActive = true;
        },
        
        deactivate: function () {
            this.$el.removeClass('active');
            this.isActive = false;
        },
        
        remove: function () {
            // We delete the element. We check check whether it is the currently
            // selected element, if yes we reset the active element.
            if (this.parentView.selected === this) {
                this.parentView.selected = null;
            }
            this.model.destroy();
            this.$el.fadeOut('slow', function () {
                this.$el.empty().remove();
            }.bind(this));
        }
    });
    
    //
    // Uploader
    // ========
    // The main application view tided to the window model
    
    var Uploader = Backbone.View.extend({
        
        el: '#media-upload-modal',
        
        selected: null,
        
        items: {}, // Stores a list view of moddels connected through ID
        
        // Additional options for the uploader. Here we can set the callback for
        // an external application, e.g. a function that adds the selected image
        // in the editor. The currently selected model will be passed into the
        // model.
        options: {
            onSubmit: function (item) {
                console.log(item);
            }
        },
        
        // Initialization of the application. To this method, additional parameters
        // in the form of an object can be passed. The most frequently used will be
        // callback onSubmit.
        initialize: function (options) {
            
            var url = ''; // Collection url that will be passed to the Dropzone.
            
            // We overwrite the default options if the user has defined his/her own.
            _.extend(this.options, options);
            
            // Redies the DOM
            this.$el.modal({show:false});
            this.$el.find('#tabs').tabs();
            this.collection = new MediaCollection();
            this.listenTo(this.collection, 'add', this.renderItem);
            this.$submit = this.$el.find('.submit-btn');
            this.collection.fetch();
            // Submits the form - we chose the image and we send it to the
            // callback.
            this.$submit.on('click', function (e) {
                e.preventDefault();
                this.submit();
            }.bind(this));
            
            // Dropzone (uploader) element ready
            url = this.collection.url;
            this.dropzone = new Dropzone('#dropzone-input', {url: url});
            this.dropzone.on('complete', function () {
                // Add the images uploaded by the user, display them
                // in the gallery and open a tab with images
                this.collection.fetch();
                this.$el.find('[href="#tabs-2"]').trigger('click');
            }.bind(this));
            // A hack to prevent 'dropzone already attached'
            $('#dropzone-input').addClass('dropzone');
        },
        
        renderItems: function (items) {
            items.each(function (item) {
                this.renderItem(item);
            }, this);
        },
        
        renderItem: function (item) {
            var picture = new MediaItem({
                model: item
            });
            picture.parentView = this;
            $(picture.render().el).appendTo(this.$el.find('#tabs-2'));
            // Here we join the view with the location element
            this.items[item.get('id')] = picture;
        },
        
        markSelected: function (view) {
            // A method that allows to select (choose) an image from the
            // collection. If we do not pass any view (from this.items list),
            // all active elements will be deselected. 
            var view = view || false;
            
            this.seleted = null;
            
            // We deselect inactive elements
            _.each(this.items, function (item) {
                if (item.isActive) {
                    item.deactivate();
                }
            }, this);
            
            // If the user clicked on an image in the gallery, we select it.
            if (view) {
                this.selected = view;
                view.activate();
            }
        },
        
        submit: function () {
            // The user has chosen an image and has submitted the form.
            if (typeof(this.options.onSubmit) === 'function') {
                var picture = {url: '', name: ''};
                if (!_.isNull(this.selected)) {
                    picture = this.selected.model.attributes;
                }
                this.options.onSubmit(picture);
            }
        },
        
        open: function () {
            // Show the uploaded window.
            this.$el.modal('show');
        },
        
        close: function () {
            // We close the window and reset the state. From unknown reasons
            // the markSelected method does not work here as expected
            this.$el.modal('hide');
            this.markSelected();
        }
    });
    
    return Uploader;
}); 