# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0019_jampick'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_cycle',
            field=models.BooleanField(default=False),
        ),
    ]
