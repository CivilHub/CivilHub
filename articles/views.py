# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from .models import Article


class BlogListView(ListView):
    """ """
    queryset = Article.objects.filter(category__name='Blog')
    context_object_name = "articles"
    template_name = "articles/blog.html"


class BlogEntryView(DetailView):
    """ """
    queryset = Article.objects.filter(category__name='Blog')
    template_name = "articles/article.html"

    def get_context_data(self, **kwargs):
        context = super(BlogEntryView, self).get_context_data(**kwargs)
        context['content_type'] = ContentType.objects.get_for_model(Article).pk
        return context


class SupportListView(ListView):
    """ """
    queryset = Article.objects.filter(category__name='Support')
    context_object_name = "articles"
    template_name = "articles/support.html"


class SupportEntryView(DetailView):
    """ """
    queryset = Article.objects.filter(category__name='Support')
    template_name = "articles/entry.html"


class TopLevelArticleView(DetailView):
    """ """
    queryset = Article.objects.all()
    article_slug = None
    template_name = "articles/article.html"

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, slug=self.article_slug)
        return article

    def get_context_data(self, **kwargs):
        context = super(TopLevelArticleView, self).get_context_data(**kwargs)
        context['content_type'] = ContentType.objects.get_for_model(Article).pk
        return context
