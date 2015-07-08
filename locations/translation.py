# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions
from .models import ImageLicense


class LicenseTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(ImageLicense, LicenseTranslationOptions)
