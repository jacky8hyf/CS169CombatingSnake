# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('roomId', models.AutoField(serialize=False, primary_key=True)),
                ('capacity', models.IntegerField(default=8)),
                ('status', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('pwhash', models.CharField(max_length=69)),
                ('nickname', models.CharField(max_length=64)),
                ('inroom', models.ForeignKey(to='gameStart.Room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='creator',
            field=models.ForeignKey(to='gameStart.User'),
        ),
    ]
