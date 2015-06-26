from django.contrib import admin
from django.utils.translation import ugettext as _

from ordered_model.admin import OrderedModelAdmin

from .models import Poll, SimplePoll, SimplePollQuestion, \
                    SimplePollAnswer, SimplePollAnswerSet


admin.site.register(SimplePollAnswer)


class PollAdmin(admin.ModelAdmin):
    search_fields = ('question', )
    list_filter = ('date_created', )
    list_display = ('__unicode__', 'get_username', 'location', 'date_created', )

    def get_username(self, obj):
        return obj.creator.get_full_name()
    get_username.short_description = _(u"user")

admin.site.register(Poll, PollAdmin)


class SimplePollAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

admin.site.register(SimplePoll, SimplePollAdmin)


class SimplePollInlineAnswerAdmin(admin.TabularInline):
    model = SimplePollAnswer
    list_display = ('text', 'move_up_down_links', )


class SimplePollQuestionAdmin(OrderedModelAdmin):
    list_display = ('text', 'question_type', 'move_up_down_links', )
    inlines = (SimplePollInlineAnswerAdmin, )

admin.site.register(SimplePollQuestion, SimplePollQuestionAdmin)


class SimplePollAnswerSetAdmin(admin.ModelAdmin):
    list_filter = ('poll', )
    list_display = ('user_full_name', 'poll', 'question', 'get_answers')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', )

    def get_answers(self, obj):
        if obj.question.question_type == 3:
            return obj.answer
        answer_ids = [int(x.strip()) for x in obj.answer.split(',')]
        answers = SimplePollAnswer.objects.filter(pk__in=answer_ids)
        return ", ".join([x.__unicode__() for x in answers])
    get_answers.short_description = _(u"answers")

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = _(u"user")

admin.site.register(SimplePollAnswerSet, SimplePollAnswerSetAdmin)
