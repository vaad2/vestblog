# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0009_article_github_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='github_link',
            new_name='github_url',
        ),
    ]
