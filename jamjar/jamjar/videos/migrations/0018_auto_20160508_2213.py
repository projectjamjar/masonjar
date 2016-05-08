# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0017_jamjarmap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoflag',
            name='flag_type',
            field=models.CharField(max_length=1, choices=[(b'Q', b'Quality'), (b'I', b'Inappropriate'), (b'A', b'Accuracy'), (b'U', b'Report User')]),
        ),
    ]
