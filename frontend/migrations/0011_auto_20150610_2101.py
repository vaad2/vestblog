# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0010_auto_20150309_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('pos', models.PositiveIntegerField(default=0, verbose_name='pos')),
                ('since', models.DateTimeField(auto_now_add=True, verbose_name='since')),
                ('title_ru', models.CharField(max_length=255, verbose_name='title ru')),
                ('title_en', models.CharField(max_length=255, verbose_name='title en', blank=True)),
                ('content_ru', models.TextField(verbose_name='content ru')),
                ('content_en', models.TextField(verbose_name='content ru', blank=True)),
                ('article', models.ForeignKey(verbose_name='article', blank=True, to='frontend.Article', null=True)),
            ],
            options={
                'verbose_name': 'poll',
                'verbose_name_plural': 'polls',
            },
            bases=(common.models.LocaleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_id', models.CharField(max_length=255, verbose_name='session id')),
                ('poll', models.ForeignKey(verbose_name='poll', to='frontend.Poll')),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-id'], 'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
    ]
