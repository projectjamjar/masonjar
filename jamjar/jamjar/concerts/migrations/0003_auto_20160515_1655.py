# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0005_auto_20160411_0257'),
        ('concerts', '0002_sponsoredevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsoredevent',
            name='artist',
        ),
        migrations.AddField(
            model_name='sponsoredevent',
            name='artists',
            field=models.ManyToManyField(related_name='sponsored_events', to='artists.Artist'),
        ),
    ]
