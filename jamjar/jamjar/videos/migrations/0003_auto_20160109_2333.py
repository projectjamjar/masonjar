# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20151128_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='hls_src',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AlterField(
            model_name='video',
            name='web_src',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
