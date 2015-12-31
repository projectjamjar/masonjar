# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(unique=True, max_length=25, verbose_name=b'username')),
                ('email', models.EmailField(unique=True, max_length=100, verbose_name=b'email address')),
                ('first_name', models.CharField(max_length=50, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=50, verbose_name=b'last name', blank=True)),
                ('is_active', models.BooleanField(default=False, help_text=b'Designates whether this user should be treated as active. Will be true once user has activated their account.', verbose_name=b'active')),
                ('is_deleted', models.BooleanField(default=False, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'deleted')),
                ('first_login', models.BooleanField(default=True, help_text=b'Whether or not this is the users first login')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
