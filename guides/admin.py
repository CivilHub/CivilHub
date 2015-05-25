# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Guide, GuideCategory, GuideTag


class GuideAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


admin.site.register(Guide, GuideAdmin)
admin.site.register(GuideCategory)
admin.site.register(GuideTag)
