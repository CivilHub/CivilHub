//
// avatarForm.js
// =============
//
// Change/edit user avatar.
//
define(['jquery',
        'underscore',
        'backbone',
        'bootstrap',
        'liquid'],

function ($, _, Backbone) {
    
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
                that.setAvatar();
            });
            this.$form.on('submit', function (e) {
                e.preventDefault();
                that.uploadAvatar();
            });
            this.$el.find('.submit-btn').on('click', function (e) {
                e.preventDefault();
                that.$form.submit();
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
            
            $(".imgLiquidFill").imgLiquid({
                fill: true,
                horizontalAlign: "center",
                verticalAlign: "top"
            });
        },
        
        uploadAvatar: function () {
            var that = this,
                formData = new FormData();
            
            // If user didn't selected any image
            if (!this.previewImg.is(':visible')) {
                this.close();
                return false;
            }
            
            formData.append('avatar', this.$uploader[0].files[0]);
            formData.append('csrfmiddlewaretoken',
                this.$form.find('[name="csrfmiddlewaretoken"]').val())
            
            $.ajax({
                type: 'POST',
                url: '/user/upload_avatar/',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    data = JSON.parse(data);
                    $('.user-thumb, .navbar-avatar').attr('src', data.avatar);
                    that.close();
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }
    });
    
    return AvatarForm;
});