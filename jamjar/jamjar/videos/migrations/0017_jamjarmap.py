# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0016_auto_20160412_0550'),
    ]

    operations = [
        migrations.CreateModel(
            name='JamJarMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.ForeignKey(related_name='startjars', to='videos.Video')),
                ('video', models.ForeignKey(related_name='jamjars', to='videos.Video')),
            ],
        ),
    ]
