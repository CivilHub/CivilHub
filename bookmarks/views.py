# -*- coding: utf-8 -*-
import json

from django.views.generic import View, ListView
from django.views.generic.edit import DeleteView
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator

from .models import Bookmark


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class BookmarkListView(LoginRequiredMixin, ListView):
    """ Widok prezentujący listę zakładek użytkownika. """
    model = Bookmark
    template_name = 'bookmarks/list.html'
    context_object_name = 'bookmarks'
    paginate_by = 25

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class BookmarkCreateView(View):
    """
    Tworzenie nowej zakładki. Widok powinien współpracować z jakimś formularzem
    JS, przyjmuje tylko dane POST od zarejestrowanego użytkownika i zwraca
    odpowiedź w formie JSON.
    """
    def post(self, request):
        if request.user.is_anonymous():
            raise Http404()
        ct = request.POST.get('content_type', None)
        pk = request.POST.get('object_id', None)
        try:
            bookmark = Bookmark.objects.create(
                user = request.user,
                object_id = pk,
                content_type = ContentType.objects.get(pk=ct)
            )
        except Exception as ex:
            bookmark = None
        if bookmark is None:
            ctx = {
                'success': False,
                'message': _(u"You can't create bookmark"),
            }
        else:
            ctx = {
                'success': True,
                'message': _(u"Bookmark created"),
                'bookmark': bookmark.pk,
            }
        return HttpResponse(json.dumps(ctx), content_type='application/json')


class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    """ Widok pozwalający użytkownikom usuwać ich zakładki. """
    model = Bookmark

    def get_success_url(self):
        return reverse('bookmarks-list')

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def post(self, request, pk=None, slug=None):
        if not request.is_ajax():
            return super(BookmarkDeleteView, self).post(request)
        bookmark = Bookmark.objects.get(pk=pk)
        if not bookmark.user == request.user:
            raise Http404()
        bookmark.delete()
        context = json.dumps({'success': True, 'message': _(u"Bookmark removed"),})
        return HttpResponse(context, content_type='application/json')
