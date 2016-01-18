# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20160117_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edge',
            name='video1',
            field=models.ForeignKey(related_name='video1', to='videos.Video'),
        ),
        migrations.AlterField(
            model_name='edge',
            name='video2',
            field=models.ForeignKey(related_name='video2', to='videos.Video'),
        ),
    ]
