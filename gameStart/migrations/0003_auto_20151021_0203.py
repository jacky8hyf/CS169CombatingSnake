# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameStart', '0002_user_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='inroom',
        ),
        migrations.RemoveField(
            model_name='user',
            name='session_id',
        ),
    ]
