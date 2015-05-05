from django.contrib import admin

from .models import MassEmail


class MassEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', )
    readonly_fields = ('sent_at', )

admin.site.register(MassEmail, MassEmailAdmin)
