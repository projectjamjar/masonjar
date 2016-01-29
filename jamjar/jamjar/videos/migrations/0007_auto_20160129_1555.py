# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0006_video_concert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('is_private', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='playlists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlaylistOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField()),
                ('playlist', models.ForeignKey(to='videos.Playlist')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.AddField(
            model_name='video',
            name='file_size',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='length',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlistorder',
            name='video',
            field=models.ForeignKey(to='videos.Video'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(related_name='playlists', through='videos.PlaylistOrder', to='videos.Video'),
        ),
    ]
