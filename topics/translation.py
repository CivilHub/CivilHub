# -*- coding: utf-8 -*-
#
# Model translation, created mainly with categories in mind.
#
from modeltranslation.translator import translator, TranslationOptions
from models import Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Category, CategoryTranslationOptions)
