# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import ImageLicense, Location, LocationBackgroundFile


admin.site.register(ImageLicense)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Location, LocationAdmin)


class LocationBackgroundAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'get_locations', )
    search_fields = ('location__name', )

    def get_locations(self, obj):
        return ", ".join([x.translation for x in obj.location_set.all()])
    get_locations.short_description = _(u"location")

admin.site.register(LocationBackgroundFile, LocationBackgroundAdmin)
