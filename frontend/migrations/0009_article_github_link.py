# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_auto_20150309_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='github_link',
            field=models.CharField(max_length=255, null=True, verbose_name='github link', blank=True),
            preserve_default=True,
        ),
    ]
