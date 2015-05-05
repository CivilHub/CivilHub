from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .models import Poll, SimplePoll, SimplePollQuestion, \
                    SimplePollAnswer, SimplePollAnswerSet


admin.site.register(SimplePollAnswer)
admin.site.register(Poll)


class SimplePollAdmin(admin.ModelAdmin):
    """
    """
    readonly_fields = ('slug', )

admin.site.register(SimplePoll, SimplePollAdmin)


class SimplePollInlineAnswerAdmin(admin.TabularInline):
    """
    """
    model = SimplePollAnswer
    list_display = ('text', 'move_up_down_links', )


class SimplePollQuestionAdmin(OrderedModelAdmin):
    """
    """
    list_display = ('text', 'question_type', 'move_up_down_links', )
    inlines = (SimplePollInlineAnswerAdmin, )

admin.site.register(SimplePollQuestion, SimplePollQuestionAdmin)


class SimplePollAnswerSetAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('user', 'poll', 'question', )

admin.site.register(SimplePollAnswerSet, SimplePollAnswerSetAdmin)
