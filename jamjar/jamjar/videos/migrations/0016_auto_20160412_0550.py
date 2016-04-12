# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_auto_20160411_0157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-created_at']},
        ),
    ]
