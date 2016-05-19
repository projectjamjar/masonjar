# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0005_auto_20160411_0257'),
        ('concerts', '0003_auto_20160515_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='artists',
            field=models.ManyToManyField(related_name='concerts', to='artists.Artist'),
        ),
    ]
