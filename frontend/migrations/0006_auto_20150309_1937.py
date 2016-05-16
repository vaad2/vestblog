# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_article_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='url',
        ),
        migrations.AddField(
            model_name='category',
            name='slug_en',
            field=models.SlugField(max_length=255, null=True, verbose_name='slug en', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='slug_ru',
            field=models.SlugField(max_length=255, null=True, verbose_name='slug ru', blank=True),
            preserve_default=True,
        ),
    ]
