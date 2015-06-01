# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from etherpad.models import Pad
from gallery.models import ContentObjectGallery, ContentObjectPicture
from organizations.models import Organization
from places_core.forms import BootstrapBaseForm

from .models import Attachment, SocialProject, TaskGroup, Task, \
                    SocialForumTopic, SocialForumEntry


class CreateProjectForm(forms.ModelForm, BootstrapBaseForm):
    """ Creation of new projects, part of the data is autocompleted. """

    class Meta:
        model = SocialProject
        fields = ('name', 'description', 'creator', 'location', 'idea', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'creator': forms.HiddenInput(),
            'location': forms.HiddenInput(),
            'idea': forms.HiddenInput(),
        }


class UpdateProjectForm(forms.ModelForm, BootstrapBaseForm):
    """ The edition of already existing projects has a different field set. """

    class Meta:
        model = SocialProject
        fields = ('name', 'description', 'is_done', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'is_done': forms.CheckboxInput(
                attrs={'class': 'custom-bs-switch'}),
        }


class TaskGroupForm(forms.ModelForm, BootstrapBaseForm):
    """ Creation and edition of group tasks."""

    class Meta:
        model = TaskGroup
        fields = ('name', 'description', 'project', 'creator', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'creator': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }


class TaskForm(forms.ModelForm, BootstrapBaseForm):
    """ Creation/edition of a task. """

    class Meta:
        model = Task
        exclude = ('participants', 'is_done', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'date_limited': forms.TextInput(
                attrs={'class': 'form-control custom-datepicker'}),
            'creator': forms.HiddenInput(),
            'group': forms.HiddenInput(),
        }


class SocialForumCreateForm(forms.ModelForm, BootstrapBaseForm):
    """ Creation/edition of a discussion in a project. """

    class Meta:
        model = SocialForumTopic
        exclude = ('slug', 'is_closed', 'creator', 'project', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
        }


class SocialForumUpdateForm(forms.ModelForm, BootstrapBaseForm):
    """ A form similar to the one above but this one offers an option to close the discussion. """

    class Meta:
        model = SocialForumTopic
        exclude = ('slug', 'creator', 'project', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'}),
            'is_closed': forms.CheckboxInput(
                attrs={'class': 'custom-bs-switch'}),
        }


class DiscussionAnswerForm(forms.ModelForm, BootstrapBaseForm):
    """ Responding to discussions - creation and edition of entries. """

    class Meta:
        model = SocialForumEntry
        fields = ('content', 'topic', 'creator', )
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'topic': forms.HiddenInput(),
            'creator': forms.HiddenInput(),
        }


class DocumentForm(forms.ModelForm):
    """ Form that cooperates with Ajax view and crates new document. """

    class Meta:
        model = Pad
        exclude = ('slug', )
        widgets = {'group': forms.HiddenInput(), }


class ProjectNGOForm(forms.Form):
    """ Allow privileged users to add project to organizations they manage. """
    project = forms.ModelChoiceField(queryset=SocialProject.objects.all(),
                                     widget=forms.HiddenInput())
    organization = forms.ModelChoiceField(queryset=Organization.objects.all())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProjectNGOForm, self).__init__(*args, **kwargs)
        self.fields['organization'].queryset = \
            Organization.objects.filter(creator=self.request.user)

    def is_valid(self):
        valid = super(ProjectNGOForm, self).is_valid()
        if not valid:
            return valid
        organization = self.cleaned_data['organization']
        user = self.request.user
        if not user.is_authenticated():
            raise forms.ValidationError(_(u"You have to be logged in"))
        if not organization.has_access(user):
            raise forms.ValidationError(
                _(u"You don't have permission to do that"))
        return True

    def save(self, *args, **kwargs):
        organization = self.cleaned_data['organization']
        project = self.cleaned_data['project']
        if not project in organization.projects.all():
            organization.projects.add(project)
        return organization


class ProjectGalleryForm(forms.ModelForm):
    """ Simplified form for gallery creation.
    """
    class Meta:
        model = ContentObjectGallery
        exclude = ('dirname', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput()
        }


class ProjectPictureForm(forms.ModelForm):
    """ This form allows users to upload gallery items.
    """
    class Meta:
        model = ContentObjectPicture
        exclude = ('gallery', 'uploaded_by', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg-no-gallery'})
        }


MAX_FILE_SIZE = 8 # In megabytes

class AttachmentUploadForm(forms.ModelForm):
    """ Upload attachment files for projects.
    """
    class Meta:
        model = Attachment
        exclude = ('mime_type', 'uploaded_by', )
        widgets = {'project': forms.HiddenInput(), }

    def clean_attachment(self):
        attachment = self.cleaned_data['attachment']
        if attachment._size > MAX_FILE_SIZE * 1024 * 1024:
            err_msg = _(u"File is too big (%d MB)" % MAX_FILE_SIZE)
            raise forms.ValidationError(err_msg)
        return attachment
