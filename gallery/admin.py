# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import LocationGalleryItem, ContentObjectGallery, ContentObjectPicture


class GalleryAdmin(admin.ModelAdmin):
    readonly_fields = ('dirname', )


admin.site.register(LocationGalleryItem)
admin.site.register(ContentObjectGallery, GalleryAdmin)
admin.site.register(ContentObjectPicture)
