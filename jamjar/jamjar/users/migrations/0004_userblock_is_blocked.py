# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='userblock',
            name='is_blocked',
            field=models.BooleanField(default=True),
        ),
    ]
