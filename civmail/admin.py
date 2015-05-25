# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from .forms import TestSendMailForm
from .models import MassEmail


class CivmailAdminSite(admin.AdminSite):
    site_header = 'Monty Python administration'
    template_name = 'civmail/civmail_admin_index.html'
    form_class = TestSendMailForm

    def get_urls(self):
        urls = super(CivmailAdminSite, self).get_urls()
        civ_urls = patterns('', (r'^emails/$', self.list_emails),
                            (r'^send/$', self.send), )
        return civ_urls + urls

    def list_emails(self, request):
        context = {'current_app': self.name, 'form': self.form_class(), }
        return render(request, self.template_name, context)

    def send(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = {'current_app': self.name, 'form': form, }
            return render(request, self.template_name, context)
        messages.add_message(request, messages.SUCCESS, _(u"emails sent"))
        return redirect('/civmail-admin/emails/')


civmail_admin_site = CivmailAdminSite(name='civadmin')


class MassEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', )
    readonly_fields = ('sent_at', )


admin.site.register(MassEmail, MassEmailAdmin)
