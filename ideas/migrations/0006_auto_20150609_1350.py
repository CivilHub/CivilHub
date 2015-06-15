# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_vote_statuses(apps, schema_editor):
    Vote = apps.get_model("ideas", "Vote")
    for vote in Vote.objects.all():
        if vote.vote:
            vote.status = 1
        else:
            vote.status = 2
        vote.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0005_vote_status'),
    ]

    operations = [
        migrations.RunPython(update_vote_statuses),
    ]
