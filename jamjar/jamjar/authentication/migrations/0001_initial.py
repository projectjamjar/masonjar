# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JamJarToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=50)),
                ('token_type', models.CharField(max_length=1, verbose_name=b'Type of token', choices=[(b'R', b'password reset'), (b'A', b'activation'), (b'I', b'invite')])),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255)),
                ('message', models.CharField(max_length=500)),
                ('accepted', models.NullBooleanField()),
                ('invitor', models.ForeignKey(related_name='sent_invites', to=settings.AUTH_USER_MODEL)),
                ('token', models.ForeignKey(related_name='invite', to='authentication.JamJarToken')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='jamjartoken',
            unique_together=set([('token', 'token_type')]),
        ),
    ]
