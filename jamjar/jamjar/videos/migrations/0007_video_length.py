# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_video_concert'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='length',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
