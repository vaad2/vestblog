# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.thread_locals
import common.utils
from django.conf import settings
import common.models
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('common', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('pos', models.PositiveIntegerField(default=0, verbose_name='pos')),
                ('since', models.DateTimeField(auto_now_add=True, verbose_name='since')),
                ('slug_ru', models.CharField(unique=True, max_length=255, verbose_name='slug ru')),
                ('slug_en', models.CharField(unique=True, max_length=255, verbose_name='slug en')),
                ('title_ru', models.CharField(max_length=255, verbose_name='title ru', blank=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='title en', blank=True)),
                ('content_ru', models.TextField(verbose_name='content ru', blank=True)),
                ('content_en', models.TextField(verbose_name='content en', blank=True)),
                ('user', models.ForeignKey(default=common.thread_locals.get_current_user, verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pos'],
                'abstract': False,
            },
            bases=(common.models.LocaleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('pos', models.PositiveIntegerField(default=0, verbose_name='pos')),
                ('since', models.DateTimeField(auto_now_add=True, verbose_name='since')),
                ('level', models.PositiveIntegerField(default=0, verbose_name='level')),
                ('path', models.TextField(verbose_name='path', blank=True)),
                ('inner_pos', models.CharField(default=b'', max_length=255, verbose_name='inner pos', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('url', models.CharField(max_length=255, null=True, verbose_name='url', blank=True)),
                ('image', common.fields.ExImageField(null=True, upload_to=common.utils.UploadPath(sub_path=b'category_icon', name_gen=True, field_name=b'self'), blank=True)),
                ('link', models.ForeignKey(related_name='category_link', blank=True, to='frontend.Category', null=True)),
                ('parent', models.ForeignKey(related_name='parent_node', verbose_name='parent', blank=True, to='frontend.Category', null=True)),
                ('site', models.ForeignKey(default=common.thread_locals.get_current_site, blank=True, to='sites.Site', null=True, verbose_name='site')),
                ('user', models.ForeignKey(default=common.thread_locals.get_current_user, verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['site', 'inner_pos', 'pos', 'title'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('pos', models.PositiveIntegerField(default=0, verbose_name='pos')),
                ('since', models.DateTimeField(auto_now_add=True, verbose_name='since')),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='title', blank=True)),
                ('content', models.TextField(verbose_name='content', blank=True)),
                ('is_content_template', models.BooleanField(default=False, verbose_name='is content template')),
                ('position_nav', models.PositiveSmallIntegerField(default=1, verbose_name='navigation position', choices=[(1, 'top'), (2, 'bottom'), (4, 'left'), (8, 'right'), (16, 'free'), (127, 'all')])),
                ('position_content', models.PositiveSmallIntegerField(default=1, verbose_name='content position', choices=[(1, 'top'), (2, 'bottom'), (4, 'left'), (8, 'right'), (16, 'free'), (127, 'all')])),
                ('nav_title', models.CharField(max_length=255, verbose_name='nav title', blank=True)),
                ('nav_show', models.BooleanField(default=True, verbose_name='nav show')),
                ('extra_pos', models.PositiveIntegerField(default=0, verbose_name='extra pos', blank=True)),
                ('seo_keywords', models.CharField(max_length=255, verbose_name='seo keywords', blank=True)),
                ('seo_description', models.CharField(max_length=255, verbose_name='seo description', blank=True)),
                ('seo_title', models.CharField(max_length=255, verbose_name='seo title', blank=True)),
                ('site', models.ForeignKey(default=common.thread_locals.get_current_site, blank=True, to='sites.Site', null=True, verbose_name='site')),
                ('site_template', models.ForeignKey(verbose_name='site template', blank=True, to='common.SiteTemplate', null=True)),
                ('user', models.ForeignKey(default=common.thread_locals.get_current_user, verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('position_nav', 'pos', 'position_content', 'seo_title'),
                'abstract': False,
                'verbose_name': 'simple page',
                'verbose_name_plural': 'simple pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('pos', models.PositiveIntegerField(default=0, verbose_name='pos')),
                ('since', models.DateTimeField(auto_now_add=True, verbose_name='since')),
                ('slug', models.CharField(unique=True, max_length=255, verbose_name='slug')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('user', models.ForeignKey(default=common.thread_locals.get_current_user, verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'slider',
                'verbose_name_plural': 'sliders',
            },
            bases=(models.Model,),
        ),
    ]
