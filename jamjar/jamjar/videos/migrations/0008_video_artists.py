# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
        ('videos', '0007_auto_20160129_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='artists',
            field=models.ManyToManyField(related_name='videos', to='artists.Artist'),
        ),
    ]
