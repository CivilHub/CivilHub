# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import AbuseReport, SearchTermRecord


admin.site.register(AbuseReport)


class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ip_address', 'get_user_full_name', )
    search_fields = ('term', )

    def get_user_full_name(self, obj):
        if obj.user is None:
            return "(%s)" % _(u"None")
        return obj.user.get_full_name()
    get_user_full_name.short_description = "user"


admin.site.register(SearchTermRecord, SearchTermAdmin)
