from django.contrib import admin
from .models import EtherpadGroup, EtherpadAuthor, Pad

class EtherpadGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('etherpad_id',)

class EtherpadAuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('etherpad_id',)

admin.site.register(EtherpadGroup, EtherpadGroupAdmin)
admin.site.register(EtherpadAuthor, EtherpadAuthorAdmin)
admin.site.register(Pad)
