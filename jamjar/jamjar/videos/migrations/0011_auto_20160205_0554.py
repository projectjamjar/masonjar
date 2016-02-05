# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0010_auto_20160204_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='hls_src',
        ),
        migrations.RemoveField(
            model_name='video',
            name='thumb_src',
        ),
        migrations.RemoveField(
            model_name='video',
            name='tmp_src',
        ),
        migrations.RemoveField(
            model_name='video',
            name='web_src',
        ),
        migrations.AddField(
            model_name='video',
            name='original_filename',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
