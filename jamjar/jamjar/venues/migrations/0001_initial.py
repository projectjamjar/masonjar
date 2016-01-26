# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('place_id', models.CharField(max_length=100, null=True, blank=True)),
                ('formatted_address', models.CharField(max_length=1000, null=True, blank=True)),
                ('lat', models.DecimalField(null=True, max_digits=12, decimal_places=8)),
                ('lng', models.DecimalField(null=True, max_digits=12, decimal_places=8)),
                ('utc_offset', models.IntegerField(null=True)),
                ('website', models.URLField(null=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('state_short', models.CharField(max_length=10, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('country_short', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
