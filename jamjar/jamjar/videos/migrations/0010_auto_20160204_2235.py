# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_auto_20160204_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file_size',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='length',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
