# from common.cachedtree import CacheTree
from django.db.models import Q
import re
from django.utils import translation
from common.utils import lang_get
from frontend.models import Category, SimplePage
from django.conf import settings
import logging

logger = logging.getLogger('middleware')

# class MiddlewareCachedTree(object):
# def process_request(self, request):
#         request.cached_tree = CacheTree(Category.tree_get(params={'state':True}), url=request.path)


class MiddlewareSimplePage(object):
    def process_request(self, request):
        try:
            if not hasattr(request, 'simple_page'):
                request.simple_page = None

            url = re.sub(r'/+', '/', '/%s/' % request.path_info.strip('/'), re.IGNORECASE)
            sps = []
            #check_re

            #check if this seller subdomain
            #qset = SimplePage.site_objects.filter(url=url, state=True)
            #ahtung distinct!!!
            qset = SimplePage.active_objects.filter(Q(url=url) | Q(category__url=url) | Q(url=request.path),
                                                    state=True).distinct()

            for idx, sp in enumerate(qset):
                sps.append(sp)

            if len(sps):
                request.simple_page = sps  #deprecated
                request.vt_sps = sps
        except SimplePage.DoesNotExist:
            request.simple_page = None


class MiddlewareCategory(object):
    def process_request(self, request):

        try:
            request.vt_category = Category.objects.get(url=request.path)
        except BaseException, e:
            request.vt_category = None


class MiddlewareLocale(object):
    def process_request(self, request):

        sr = re.search('^/([A-Za-z]{2})/', request.path)
        lang_dc = dict(item for item in settings.LANGUAGES)

        request.vt_lang = sr.group(1) if sr and sr.group(1) in lang_dc else settings.LANGUAGE_CODE

        translation.activate(request.vt_lang)

class MiddlewareSessionExist(object):
    def process_request(self, request):

        request.session['init'] = 1