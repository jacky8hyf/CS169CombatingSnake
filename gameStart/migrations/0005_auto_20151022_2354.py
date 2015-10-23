# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameStart', '0004_auto_20151021_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='inroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='gameStart.Room', null=True),
        ),
    ]
