# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20160201_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='length',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
