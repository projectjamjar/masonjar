# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0018_auto_20160508_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='JamPick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('video', models.ForeignKey(related_name='jampick', to='videos.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
