import ujson
from django.utils.datastructures import SortedDict
import jinja2
import logging

from collections import OrderedDict

from django_jinja import library
from django.conf import settings

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.templatetags.thumbnail import margin
from common.utils import lang_get
from frontend.models import Article, Category
# import markdown2
# import markdown

logger = logging.getLogger('rxshop.tags')

@jinja2.contextfunction
@library.global_function
def tag_article_list(ctx):
    return Article.active_objects.all()



@jinja2.contextfunction
@library.global_function
def tag_category_list(ctx):
    return Category.objects.order_by('title_%s' % lang_get())


@library.filter
def markdown(content):
    import markdown
    return  markdown.markdown(content, ['codehilite(css_class=highlight)', 'extra'])
    # return  markdown.markdown(content, ['codehilite'])


# @jinja2.contextfilter
# @library.filter
# def currency(ctx, val):
#     return rx_format_currency(ctx['request'], val)
#     # return format_currency(val, ctx['request'].session[settings.CURRENCY_SESSION_KEY], locale=lng_get())
#
#     # context['menu_product_list'] = self.get_queryset()
#
