# -*- coding: utf-8 -*-
#
# Tłumaczenia dla modeli, głównie z myślą o kategoriach.
#
from modeltranslation.translator import translator, TranslationOptions
from models import Badge


class BadgeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Badge, BadgeTranslationOptions)
