# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_auto_20150610_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='num_votes',
            field=models.PositiveIntegerField(default=0, verbose_name='num votes'),
            preserve_default=True,
        ),
    ]
