# -*- coding: utf-8 -*-
#
# Tłumaczenia dla modeli, głównie z myślą o kategoriach.
#
from modeltranslation.translator import translator, TranslationOptions
from models import Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Category, CategoryTranslationOptions)
