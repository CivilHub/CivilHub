//
// avatarForm.js
// =============
//
// Change/edit user avatar.
//
define(['jquery',
        'underscore',
        'backbone',
        'bootstrap'],

function ($, _, Backbone, utils) {
    
    "use strict";
    
    var AvatarForm = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'modal fade',
        
        template: _.template($('#avatar-form-tpl').html()),
        
        initialize: function () {
            this.render();
            var that = this;
            this.$form = this.$el.find('form:first');
            this.$uploader = this.$form.find('#id_avatar');
            this.previewImg = this.$el.find('#avatar-img-placeholder');
            this.$uploader.on('change', function (e) {
                e.preventDefault();
                that.$form.submit();
            });
            this.$form.on('submit', function (e) {
                e.preventDefault();
                //that.uploadAvatar();
                that.setAvatar();
            });
        },
        
        render: function () {
            this.$el.html(this.template({}));
            this.$el.modal({show:false});
            return this;
        },
        
        open: function () {
            this.$el.modal('show');
        },
        
        close: function () {
            this.$el.modal('hide');
        },
        
        setAvatar: function () {
            var that = this;
            var img = this.$uploader[0].files[0];
            var reader = new FileReader();
            reader.onload = function (e) {
                that.previewImg.attr('src', e.target.result).show();
            }
            reader.readAsDataURL(img);
            console.log(img);
            console.log(this.previewImg);
        },
        
        uploadAvatar: function () {
            var that = this,
                formData = new FormData();
            formData.append('avatar', this.$uploader[0].files[0]);
            formData.append('csrfmiddlewaretoken',
                this.$form.find('[name="csrfmiddlewaretoken"]').val())
            alert(that.$form.attr('target'));
            $.ajax({
                type: 'POST',
                url: '/user/upload_avatar/',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data);
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }
    });
    
    return AvatarForm;
});