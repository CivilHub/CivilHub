# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from .models import MassEmail


class MassEmailTranslationOptions(TranslationOptions):
    fields = ('subject', 'body',)

translator.register(MassEmail, MassEmailTranslationOptions)
