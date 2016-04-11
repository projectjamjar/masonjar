# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0004_auto_20160411_0226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['-popularity']},
        ),
    ]
