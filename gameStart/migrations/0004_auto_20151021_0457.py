# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameStart', '0003_auto_20151021_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='inroom',
            field=models.ForeignKey(default=None, to='gameStart.Room', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='session_id',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(unique=True, max_length=64),
        ),
    ]
