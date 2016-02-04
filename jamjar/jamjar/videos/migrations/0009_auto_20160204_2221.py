# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0008_video_artists'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('flag_type', models.CharField(max_length=1, choices=[(b'Q', b'Quality'), (b'I', b'Inappropriate'), (b'A', b'Accuracy')])),
                ('notes', models.CharField(max_length=500, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='flags_submitted', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('vote', models.NullBooleanField()),
                ('user', models.ForeignKey(related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='video',
            name='thumb_src',
            field=models.URLField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='video',
            name='user',
            field=models.ForeignKey(related_name='videos', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='hls_src',
            field=models.URLField(default=b'', max_length=128),
        ),
        migrations.AlterField(
            model_name='video',
            name='web_src',
            field=models.URLField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='videovote',
            name='video',
            field=models.ForeignKey(related_name='votes', to='videos.Video'),
        ),
        migrations.AddField(
            model_name='videoflag',
            name='video',
            field=models.ForeignKey(related_name='flags', to='videos.Video'),
        ),
    ]
