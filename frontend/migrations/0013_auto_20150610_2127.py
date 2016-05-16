# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_poll_num_votes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ['-state', '-id'], 'verbose_name': 'poll', 'verbose_name_plural': 'polls'},
        ),
        migrations.AddField(
            model_name='poll',
            name='date_close',
            field=models.DateTimeField(null=True, verbose_name='date', blank=True),
            preserve_default=True,
        ),
    ]
