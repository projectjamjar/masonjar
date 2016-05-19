# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concerts', '0004_concert_artists'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='jamjars_count',
            field=models.IntegerField(default=0),
        ),
    ]
