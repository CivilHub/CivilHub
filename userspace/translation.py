# -*- coding: utf-8 -*-
#
# Model translation, created mainly with categories in mind.
#
from modeltranslation.translator import translator, TranslationOptions
from models import Badge


class BadgeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Badge, BadgeTranslationOptions)
