# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0003_auto_20150420_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255, verbose_name='key', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_accepted', models.DateTimeField(null=True, verbose_name='date accepted', blank=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name='is accepted')),
                ('organization', models.ForeignKey(related_name='invitations', verbose_name='organization', to='organizations.Organization')),
                ('user', models.ForeignKey(related_name='ngo_invitations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'invitation',
                'verbose_name_plural': 'invitations',
            },
            bases=(models.Model,),
        ),
    ]
