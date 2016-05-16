# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_auto_20150309_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug_en',
            field=models.SlugField(max_length=255, null=True, verbose_name='slug en', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='slug_ru',
            field=models.SlugField(max_length=255, null=True, verbose_name='slug ru', blank=True),
            preserve_default=True,
        ),
    ]
