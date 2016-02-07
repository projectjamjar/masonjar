# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_auto_20160205_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='artists',
            field=models.ManyToManyField(related_name='videos', to='artists.Artist', blank=True),
        ),
    ]
