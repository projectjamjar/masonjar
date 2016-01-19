# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20151128_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('video1', models.PositiveIntegerField()),
                ('video2', models.PositiveIntegerField()),
                ('offset', models.IntegerField()),
                ('confidence', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='video',
            name='uploaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='video',
            name='hls_src',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AlterField(
            model_name='video',
            name='web_src',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
