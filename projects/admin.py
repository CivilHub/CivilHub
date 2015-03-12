from django.contrib import admin
from .models import SocialProject, TaskGroup, Task

class SocialProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'creator', 'is_done',)
    readonly_fields = ('slug',)

class TaskInlineAdmin(admin.TabularInline):
    model = Task
    extra = 1

class TaskGroupAdmin(admin.ModelAdmin):
    inlines = (TaskInlineAdmin,)

admin.site.register(SocialProject, SocialProjectAdmin)
admin.site.register(TaskGroup, TaskGroupAdmin)
