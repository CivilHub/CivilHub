from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Article

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'subtitle')


translator.register(Category, CategoryTranslationOptions)
translator.register(Article, ArticleTranslationOptions)
