//
// bookmark-form.js
// ================
// Custom scripts for django-generic-bookmarks.
// Provides ajax interface for bookmark form.
//
$.fn.bookmarkForm = function () {
    "use strict";
    return $(this).each(function (options) {
        
        var $element = $(this),
        
            defaults = {
                onSubmit: function (fields) { return fields; }
            },
            
            options = $.fn.extend(defaults, options),
            
            form = {
                $el: $element,
                
                $addBtn: $element.find('.btn-add-bookmark'),
                
                $removeBtn: $element.find('.btn-remove-bookmark'),
                
                action: $element.attr('action'),
                
                serialize: function () {
                    return this.$el.serializeArray();
                },
                
                switchButtons: function (resp) {
                    var that = this;
                    if (resp.created) {
                        that.$addBtn.fadeOut('fast', function () {
                            that.$removeBtn.fadeIn('fast');
                        });
                    } else {
                        that.$removeBtn.fadeOut('fast', function () {
                            that.$addBtn.fadeIn('fast');
                        });
                    }
                },
                
                submit: function (success, error) {
                    var that = this;
                    
                    $.ajax({
                        type: 'POST',
                        
                        url: this.action,
                        
                        data: this.serialize(),
                        
                        success: function (resp) {
                            if (typeof(success) === 'function') {
                                success(resp);
                            }
                            that.switchButtons(resp);
                            return true;
                        },
                        
                        error: function (err) {
                            if (typeof(error) === 'function') {
                                error(err);
                            }
                            return false;
                        }
                    });
                }
            };
            
        $element
            .removeAttr('id')
            
            .data('bookmarkForm', form)
            
            .on('submit', function (e) {
                e.preventDefault();
                form.submit(function (resp) {
                    options.onSubmit(form.serialize());
                }, function (err) {
                    console.log(err);
                });
            });
            
        form.$addBtn.on('click', function (e) {
            e.preventDefault();
            $element.submit();
        });
        
        form.$removeBtn.on('click', function (e) {
            e.preventDefault();
            $element.submit();
        });
    });
};