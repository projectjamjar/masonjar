# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20160116_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edge',
            name='offset',
            field=models.FloatField(),
        ),
    ]
