# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Blessing


class BlessAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_full_name', 'get_content_object', 'date', )
    list_filter = ('date', )

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = _(u"user full name")

    def get_content_object(self, obj):
        if obj.content_object is None:
            return ""
        return '<a href="{}" target="_blank">{}</a>'.format(
            obj.content_object.get_absolute_url(),
            obj.content_object.__unicode__())
    get_content_object.allow_tags = True
    get_content_object.short_description = _(u"content object")

admin.site.register(Blessing, BlessAdmin)
