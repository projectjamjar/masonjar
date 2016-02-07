# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_auto_20160205_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='recorded_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='width',
            field=models.IntegerField(default=0),
        ),
    ]
