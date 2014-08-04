# -*- coding: utf-8 -*-
from django.contrib import admin
from locations.models import Location
from import_export import resources
from import_export.admin import ImportExportMixin


class AdminLocation(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Location, AdminLocation)
