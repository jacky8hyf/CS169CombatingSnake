# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameStart', '0005_auto_20151022_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='session_id',
            field=models.CharField(default=None, max_length=255, unique=True, null=True),
        ),
    ]
