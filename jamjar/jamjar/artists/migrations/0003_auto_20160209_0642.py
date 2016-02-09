# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_auto_20160208_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(max_length=500)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('artist', models.ForeignKey(related_name='images', to='artists.Artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='genre',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='modified_at',
        ),
    ]
