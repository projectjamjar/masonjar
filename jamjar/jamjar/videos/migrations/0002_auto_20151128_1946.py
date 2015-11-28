# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='src',
            new_name='tmp_src',
        ),
        migrations.AddField(
            model_name='video',
            name='hls_src',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='web_src',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
