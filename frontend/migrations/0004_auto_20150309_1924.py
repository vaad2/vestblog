# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_tag_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['site', 'inner_pos', 'pos', 'title_ru'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='title en', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='title_ru',
            field=models.CharField(default=b'', max_length=255, verbose_name='title ru'),
            preserve_default=True,
        ),
    ]
