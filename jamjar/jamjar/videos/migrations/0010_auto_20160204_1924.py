# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0009_auto_20160201_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumb_src',
            field=models.URLField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='video',
            name='user',
            field=models.ForeignKey(related_name='videos', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='hls_src',
            field=models.URLField(default=b'', max_length=128),
        ),
        migrations.AlterField(
            model_name='video',
            name='web_src',
            field=models.URLField(default=b'', max_length=128),
        ),
    ]
