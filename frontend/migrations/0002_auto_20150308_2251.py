# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_ru', models.CharField(max_length=255, verbose_name='title ru')),
                ('title_en', models.CharField(max_length=255, verbose_name='title en')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(common.models.LocaleModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='frontend.Tag', null=True, verbose_name='tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='slug_en',
            field=models.SlugField(unique=True, max_length=255, verbose_name='slug en'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='slug_ru',
            field=models.SlugField(unique=True, max_length=255, verbose_name='slug ru'),
            preserve_default=True,
        ),
    ]
