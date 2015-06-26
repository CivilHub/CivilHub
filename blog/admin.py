# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from blog.models import Category, News


admin.site.register(Category)


class NewsAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_filter = ('date_created', )
    list_display = ('__unicode__', 'get_username', 'location', 'date_created', )
    raw_id_fields = ('location', )

    def get_username(self, obj):
        return obj.creator.get_full_name()
    get_username.short_description = _(u"user")

admin.site.register(News, NewsAdmin)
