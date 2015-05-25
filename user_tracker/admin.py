# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'ip_address',
                    'session_start', 'last_update', )
    list_filter = ('last_update', )
    search_fields = ('user__first_name', 'user__last_name',
                     'user__email', 'ip_address', )
    readonly_fields = ('checked', )

    def user_full_name(self, obj):
        if obj.user is None:
            return _(u"Anonymous")
        return obj.user.get_full_name()
    user_full_name.short_description = 'user'

admin.site.register(Visitor, VisitorAdmin)
