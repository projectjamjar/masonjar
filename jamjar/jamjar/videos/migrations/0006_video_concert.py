# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concerts', '0001_initial'),
        ('videos', '0005_auto_20160118_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='concert',
            field=models.ForeignKey(related_name='concert', default=None, to='concerts.Concert'),
            preserve_default=False,
        ),
    ]
