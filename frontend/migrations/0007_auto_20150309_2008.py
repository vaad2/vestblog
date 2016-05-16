# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0006_auto_20150309_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='preview_en',
            field=models.TextField(default=b'', null=True, verbose_name='preview ru', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='preview_ru',
            field=models.TextField(default=b'', null=True, verbose_name='preview ru', blank=True),
            preserve_default=True,
        ),
    ]
