# -*- coding: utf-8 -*-
from django.contrib import admin
from locations.models import Location

class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Location, LocationAdmin)
