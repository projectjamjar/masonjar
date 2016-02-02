# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_video_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='length',
            field=models.FloatField(default=None),
        ),
    ]
