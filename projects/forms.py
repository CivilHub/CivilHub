# -*- coding: utf-8 -*-
from django import forms

from places_core.forms import BootstrapBaseForm

from .models import SocialProject, TaskGroup, Task, SocialForumTopic, SocialForumEntry


class CreateProjectForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie nowych projektów - część danych jest autouzupełniana. """
    class Meta:
        model = SocialProject
        fields = ('name', 'description', 'creator', 'location',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'creator': forms.HiddenInput(),
            'location': forms.HiddenInput(),
        }


class UpdateProjectForm(forms.ModelForm, BootstrapBaseForm):
    """ Edycja istniejących projektów ma inny zestaw pól. """
    class Meta:
        model = SocialProject
        fields = ('name', 'description', 'is_done',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'custom-bs-switch'}),
        }


class TaskGroupForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie oraz edycja grup zadań. """
    class Meta:
        model = TaskGroup
        fields = ('name', 'description', 'project', 'creator',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'creator': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }


class TaskForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie/edycja zadania. """
    class Meta:
        model = Task
        exclude = ('participants', 'is_done',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'date_limited': forms.TextInput(attrs={'class': 'form-control custom-datepicker'}),
            'creator': forms.HiddenInput(),
            'group': forms.HiddenInput(),
        }


class SocialForumCreateForm(forms.ModelForm, BootstrapBaseForm):
    """ Tworzenie/edycja dyskusji w ramach projektu. """
    class Meta:
        model = SocialForumTopic
        exclude = ('slug', 'is_closed', 'creator', 'project',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
        }


class SocialForumUpdateForm(forms.ModelForm, BootstrapBaseForm):
    """ Formularz podobny do powyższego, ale oferujący opcję zamknięcia dyskusji. """
    class Meta:
        model = SocialForumTopic
        exclude = ('slug', 'creator', 'project',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'is_closed': forms.CheckboxInput(attrs={'class': 'custom-bs-switch'}),
        }


class DiscussionAnswerForm(forms.ModelForm, BootstrapBaseForm):
    """ Odpowiadanie na dyskusje - tworzenie i edycja wpisów. """
    class Meta:
        model = SocialForumEntry
        fields = ('content', 'topic', 'creator',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'topic': forms.HiddenInput(),
            'creator': forms.HiddenInput(),
        }
