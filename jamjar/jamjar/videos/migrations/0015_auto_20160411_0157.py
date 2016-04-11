# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_auto_20160207_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='concert',
            field=models.ForeignKey(related_name='videos', to='concerts.Concert'),
        ),
    ]
