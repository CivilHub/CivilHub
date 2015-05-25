# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from .models import SimplePoll, SimplePollQuestion, SimplePollAnswer


class SimplePollTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(SimplePoll, SimplePollTranslationOptions)


class SimplePollQuestionTranslationOptions(TranslationOptions):
    fields = ('text', )

translator.register(SimplePollQuestion, SimplePollQuestionTranslationOptions)


class SimplePollAnswerTranslationOptions(TranslationOptions):
    fields = ('text', )

translator.register(SimplePollAnswer, SimplePollAnswerTranslationOptions)
