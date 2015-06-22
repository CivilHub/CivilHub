# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blessing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='recommendations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'recommendation',
                'verbose_name_plural': 'recommendations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='blessing',
            unique_together=set([('user', 'content_type', 'object_pk')]),
        ),
    ]
