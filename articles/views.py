# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from .models import Category, Article


def expand_category_tree(category):
    """
    This function returns dictionary of elements containing all subcategories of
    selected category passed as argument and links related to articles belonging
    to these categories. Returns dictionary content which could be included in
    template. Function run recursively from top (provided category instance) 
    to bottom (last article in tree).
    """
    links = {
        'category': {
            'name': category.name,
            'level': category.level,
        },
        'subcategories': [],
        'articles': [],
    }
    for sub in category.subcategories.all():
        links['subcategories'].append(expand_category_tree(sub))
    for art in category.article_set.all():
        article_link = {
            'title': art.title,
            'url': art.get_absolute_url(),
        }
        links['articles'].append(article_link)
    return links


def print_category_tree(category):
    """
    This function returns HTML tree structure related to selected category and
    divided into links for subcategories and for single articles.
    """
    art_tpl = '<li class="article-link"><a href="{}">{}</a></li>'
    html = '<li class="category-entry"><a href="#">{}</a><ul class="sublist sub-lvl-{}">' \
            .format(category.name, category.level)
    for cat in category.subcategories.all():
        html += print_category_tree(cat)
    for article in category.article_set.all():
        html += art_tpl.format(article.get_absolute_url(), article.title)
    return html + '</ul></li>'


def print_menu(category):
    """
    Function returns HTML content for entire menu for selected category. Made
    to be used with Support section. This way we can omit parent category and
    display just categories related to this one.
    """
    html = ''
    for sub in category.subcategories.all():
        html += print_category_tree(sub)
    return html


class SupportListView(TemplateView):
    """ Show list of support and help topics. """
    template_name = "articles/support.html"

    def get_context_data(self, **kwargs):
        context = super(SupportListView, self).get_context_data(**kwargs)
        context['title'] = _("Help and support")
        try:
            category = Category.objects.get(name__icontains=u'support')
            context['menu'] = print_menu(category)
        except Category.DoesNotExist:
            context['menu'] = _("Support category does not exist yet")
        return context


class SupportEntryView(DetailView):
    """ Detailed support entry about specific topic. """
    model = Article
    template_name = "articles/entry.html"

    def get_context_data(self, **kwargs):
        context = super(SupportEntryView, self).get_context_data(**kwargs)
        context['articles'] = self.get_object().category.article_set.all()
        return context


class BlogListView(ListView):
    """ Manage list of all blog entries. """
    queryset = Article.objects.filter(category__name='Blog')
    context_object_name = "articles"
    template_name = "articles/blog.html"


class BlogEntryView(DetailView):
    """ Display single blog entry. """
    queryset = Article.objects.filter(category__name='Blog')
    template_name = "articles/article-blog.html"


class TopLevelArticleView(DetailView):
    """
    View for each item to be shown regardless of the category
    or support work. It can be easily extended giving 'article_slug' and possibly
    'template_name' in the configuration URL (see urls.py).
    """
    model = Article
    article_slug = None
    template_name = "articles/article.html"

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, slug=self.article_slug)
        return article
