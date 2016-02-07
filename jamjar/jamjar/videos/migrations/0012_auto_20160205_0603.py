# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_auto_20160205_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='artists',
            field=models.ManyToManyField(related_name='videos', null=True, to='artists.Artist', blank=True),
        ),
    ]
