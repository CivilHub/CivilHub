from django.contrib import admin
from django.utils.translation import ugettext as _
from .models import Category, Discussion, Entry

admin.site.register(Category)
admin.site.register(Entry)


class DiscussionAdmin(admin.ModelAdmin):
    search_fields = ('question', )
    list_filter = ('date_created', )
    list_display = ('__unicode__', 'get_username', 'location', 'date_created', )

    def get_username(self, obj):
        return obj.creator.get_full_name()
    get_username.short_description = _(u"user")

admin.site.register(Discussion, DiscussionAdmin)
