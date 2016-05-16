# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_auto_20150308_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='num',
            field=models.PositiveIntegerField(default=0, verbose_name='num'),
            preserve_default=True,
        ),
    ]
