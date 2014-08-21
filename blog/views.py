# -*- coding: utf-8 -*-
import json, datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
from django.views.generic import View, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType
from maps.forms import AjaxPointerForm
from maps.models import MapPointer
from locations.models import Location
from locations.links import LINKS_MAP as links
from .models import Category, News
from .forms import NewsForm
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from places_core.helpers import SimplePaginator, truncatehtml
# Mobile API
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from .serializers import NewsSimpleSerializer, NewsCategorySerializer


class NewsAPIView(viewsets.ModelViewSet):
    """
    Simple view for mobile applications. Provides a way to manage blog.
    """
    queryset = News.objects.all()
    serializer_class = NewsSimpleSerializer
    paginate_by = settings.PAGE_PAGINATION_LIMIT
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.creator = self.request.user


class BlogCategoryAPIViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Category.objects.all()
    serializer_class = NewsCategorySerializer
    paginate_by = None
    permission_classes = (rest_permissions.IsAdminUser,)


class BasicNewsSerializer(object):
    """
    This is custom serializer for blog entries. It passes properly formatted.
    For more detailed info check BasicIdeaSerializer in ideas.views.
    """
    def __init__(self, obj):
        tags = []

        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':obj.location.slug,
                                       'tag':tag.name})
            })

        self.data = {
            'id'            : obj.pk,
            'title'         : obj.title,
            'slug'          : obj.slug,
            'link'          : obj.get_absolute_url(),
            'description'   : truncatehtml(obj.content, 240),
            'username'      : obj.creator.username,
            'user_full_name': obj.creator.get_full_name(),
            'creator_url'   : obj.creator.profile.get_absolute_url(),
            'user_id'       : obj.creator.pk,
            'avatar'        : obj.creator.profile.avatar.url,
            'date_created'  : timesince(obj.date_created),
            'edited'        : obj.edited,
            'comment_count' : obj.get_comment_count(),
            'tags'          : tags,
        }

        try:
            self.data['date_edited'] = timesince(obj.date_edited)
        except Exception:
            self.data['date_edited'] = ''

        if obj.category:
            self.data['category']     = obj.category.name
            self.data['category_url'] = reverse('locations:category_search',
                kwargs={
                    'slug'    : obj.location.slug,
                    'app'     : 'blog',
                    'model'   : 'news',
                    'category': obj.category.pk,
                })
        else:
            self.data['category'] = ''
            self.data['category_url'] = ''


class BasicBlogView(View):
    """
    Basic view for our custom REST API, not involving Django rest framework.
    This API returns queryset in JSON format upon which backbone Blog collection
    is built.
    """
    def get_queryset(self, request, queryset):
        order = request.GET.get('order')
        time = request.GET.get('time')
        category = request.GET.get('category')
        haystack = request.GET.get('haystack')

        if category and category != 'all':
            category = Category.objects.get(pk=request.GET.get('category'))
            queryset = queryset.filter(category=category)

        time_delta = None

        if time == 'day':
            time_delta = datetime.date.today() - datetime.timedelta(days=1)
        if time == 'week':
            time_delta = datetime.date.today() - datetime.timedelta(days=7)
        if time == 'month':
            time_delta = datetime.date.today() - relativedelta(months=1)
        if time == 'year':
            time_delta = datetime.date.today() - relativedelta(years=1)

        if time_delta:
            queryset = queryset.filter(date_created__gte=time_delta)

        if haystack and haystack != 'false':
            queryset = queryset.filter(title__icontains=haystack)
        
        if order == 'title':
            return queryset.order_by('title')
        elif order == 'latest':
            return queryset.order_by('-date_created')
        elif order == 'oldest':
            return queryset.order_by('date_created')
        elif order == 'category':
            return queryset.order_by('category__name')
        elif order == 'username':
            l = list(queryset);
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l

        return queryset.order_by('-date_created')

    def get(self, request, slug=None, pk=None, *args, **kwargs):

        ctx = {'results': []}

        if not pk:
            if not slug:
                news_list = News.objects.all()
            else:
                location = Location.objects.get(slug=slug)
                news_list = News.objects.filter(location=location)

            news_list = self.get_queryset(request, news_list)

            for news in news_list:
                ctx['results'].append(BasicNewsSerializer(news).data)

            paginator = SimplePaginator(ctx['results'], settings.PAGE_PAGINATION_LIMIT)
            page = request.GET.get('page') if request.GET.get('page') else 1
            ctx['current_page'] = page
            ctx['total_pages'] = paginator.count()
            ctx['results'] = paginator.page(page)
        else:
            news = get_object_or_404(News, pk=pk)
            ctx['results'] = BasicNewsSerializer(news).data
            ctx['current_page'] = 1
            ctx['total_pages'] = 1

        return HttpResponse(json.dumps(ctx))


class CategoryListView(ListView):
    """
    Categories for place's blog
    """
    model = Category
    context_object_name = 'categories'

    
class CategoryDetailView(DetailView):
    """
    Show category info
    """
    model = Category

    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Create new category
    """
    model = Category
    fields = ['name', 'description']


class NewsListView(ListView):
    """
    News index for chosen location
    """
    model = News
    context_object_name = 'entries'

    
class NewsDetailView(DetailView):
    """
    Detailed news page
    """
    model = News

    def get_context_data(self, **kwargs):
        news = super(NewsDetailView, self).get_object()
        content_type = ContentType.objects.get_for_model(news)
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, news.location)
        context['location'] = news.location
        context['content_type'] = content_type.pk
        context['title'] = news.title
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(self.object)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(self.object),
                'object_pk'   : self.object.pk,
            })
        context['links'] = links['news']
        return context

    
class NewsCreateView(LoginRequiredMixin, CreateView):
    """
    Create new entry
    """
    model = News
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(NewsCreateView, self).form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Let owner edit his newses.
    """
    model = News
    form_class = NewsForm
    template_name = 'locations/location_news_form.html'

    def get_context_data(self, **kwargs):
        obj = super(NewsUpdateView, self).get_object()
        moderator = is_moderator(self.request.user, obj.location)
        if obj.creator != self.request.user and not moderator:
            raise PermissionDenied
        context = super(NewsUpdateView, self).get_context_data(**kwargs)
        context['is_moderator'] = moderator
        context['title'] = obj.title
        context['subtitle'] = _('Edit entry')
        context['location'] = obj.location
        context['links'] = links['news']
        return context
