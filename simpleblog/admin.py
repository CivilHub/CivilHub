from django.contrib import admin

from .models import BlogCategory, BlogEntry

admin.site.register(BlogCategory)
admin.site.register(BlogEntry)
