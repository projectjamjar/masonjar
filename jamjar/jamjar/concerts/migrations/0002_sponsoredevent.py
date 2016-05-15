# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0005_auto_20160411_0257'),
        ('concerts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsoredEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('artist', models.ForeignKey(related_name='sponsored_events', to='artists.Artist')),
                ('concert', models.ForeignKey(related_name='sponsored_event', to='concerts.Concert')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
