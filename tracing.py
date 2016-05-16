import os
from datetime import datetime
from django.forms import ImageField
from django.template import RequestContext

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vestblog.settings")

import django
django.setup()

from frontend.models import Tag, Article
# from django.core.management import call_command
# call_command('makemigrations', 'frontend')
# import markdown2
# # print markdown2.markdown("*boo!*")
# jj = dict((x,x) for x in xrange(10))
# print jj

art = Article.objects.all()[0]
mdt = Article.tag.through

for tag in art.tag.all():
    print mdt.objects.filter(tag=tag).count()
    # print tag.through.objects
# print Article.tag.through.objects.filter(article=art)


print datetime.strptime('Jan 14 2009 11:00PM', '%b %d %Y %I:%M%p')

RequestContext
ImageField
from django.core.context_processors import static