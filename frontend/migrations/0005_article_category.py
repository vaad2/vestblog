# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20150309_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=None, blank=True, to='frontend.Category', null=True, verbose_name='category'),
            preserve_default=True,
        ),
    ]
