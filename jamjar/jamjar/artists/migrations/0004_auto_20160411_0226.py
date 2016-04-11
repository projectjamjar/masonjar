# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_auto_20160209_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='followers',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='popularity',
            field=models.IntegerField(null=True),
        ),
    ]
