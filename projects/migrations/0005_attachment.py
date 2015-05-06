# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_socialproject_authors_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('attachment', models.FileField(upload_to=projects.models.get_attachment_path, max_length=200, verbose_name='file')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True, verbose_name='date uploaded')),
                ('project', models.ForeignKey(related_name='attachments', verbose_name='project', to='projects.SocialProject')),
                ('uploaded_by', models.ForeignKey(related_name='attachments', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
