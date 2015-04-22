# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView

from .forms import BlogEntryForm
from .models import BlogEntry


class BlogEntryCreateView(CreateView):
	"""
	Create new blog entry.
	"""
	model = BlogEntry
	form_class = BlogEntryForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.author = self.request.user
		return super(BlogEntryCreateView, self).form_valid(form)
