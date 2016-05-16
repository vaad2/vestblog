import urllib
from django import http
from django.core.urlresolvers import reverse, resolve
from django.middleware.locale import LocaleMiddleware
from django.utils import translation
import re
from common.thread_locals import get_current_site
from thread_locals import set_thread_var

class MiddlewareView(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            request.curr_view = view_func.__name__
            request.curr_view_url = request.path
            namespace = resolve(request.path).namespace

            request.curr_view_full = '%s:%s' % (namespace, request.curr_view)
            request.curr_view_full_ul = '%s__%s' % (namespace, request.curr_view)
#            reverse(request.curr_view)
#            request.curr_view_name = resolve_to_name(request.path)
        except BaseException, e:
            pass

class MiddlewareMultipleProxy(object):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
        ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()

class MiddlewareThreadLocal(object):
    """ Simple middleware that adds the request object in thread local storage."""
    def process_request(self, request):
        set_thread_var('request', request)

class MiddlewareAjaxCSRFDisable(object):
    def process_request(self, request):
        if request.is_ajax():
            setattr(request, '_dont_enforce_csrf_checks', True)

class MiddlewareFilterPersist(object):
    def process_request(self, request):

        if '/admin/' not in request.path:
            return None

        if not request.META.has_key('HTTP_REFERER'):
            return None

        popup = 'pop=1' in request.META['QUERY_STRING']
        path = request.path
        query_string = request.META['QUERY_STRING']
        session = request.session

        if session.get('redirected', False):#so that we dont loop once redirected
            del session['redirected']
            return None

        referrer = request.META['HTTP_REFERER'].split('?')[0]
        referrer = referrer[referrer.find('/admin'):len(referrer)]
        key = 'key'+path.replace('/','_')
        if popup:
            key = 'popup'+path.replace('/','_')

        if path == referrer: #We are in same page as before
            if query_string == '': #Filter is empty, delete it
                if session.get(key,False):
                    del session[key]
                return None
#            request.session[key] = query_string
            request.session[key] = request.GET.copy()
            request.session.modified = True
        else: #We are are coming from another page, restore filter if available
            if session.get(key, False):
#                urllib.urlencode
                try:
                    query = request.session.get(key)
                    query.update(request.GET.copy())
                    query_string = urllib.urlencode(query)
                    redirect_to = path+'?' + query_string
                    request.session['redirected'] = True
                    return http.HttpResponseRedirect(redirect_to)
                except:
                    pass
#                query_string=request.session.get(key)

        return None

class MiddlewareSite(object):
    def process_request(self, request):
        request.site = get_current_site()


class MiddlewareAppData(object):
    def process_request(self, request):
        from django.conf import settings
        request.APP_DATA = settings.APP_DATA

#operate lang switch by url
class MiddlewareLang(object):
    def process_request(self, request):
        from django.conf import settings
        langs = dict(settings.LANGUAGES)
        lang = settings.LANGUAGE_CODE.split('-')[0]

        path = request.path.split('/')
        if len(path) > 1 and path[1] in langs:
            request.lang = path[1]
        else:
            request.lang = lang

class MiddlewareSwitchLocale(LocaleMiddleware):
    def process_request(self, request):
    #        if 'language' in request.GET:
    #            request.session['django_language'] = request.GET['language']
        language = request.lang
        translation.activate(language)
        request.LANGUAGE_CODE = language

#for django admin
class MiddlewareFilterPersist(object):
    def process_request(self, request):

        if '/admin/' not in request.path:
            return None

        if not request.META.has_key('HTTP_REFERER'):
            return None

        popup = 'pop=1' in request.META['QUERY_STRING']
        path = request.path

        if  path.find('/add/') >= 0:
            return None

        query_string = request.META['QUERY_STRING']
        session = request.session

        if session.get('redirected', False):#so that we dont loop once redirected
            del session['redirected']
            return None

        referrer = request.META['HTTP_REFERER'].split('?')[0]
        referrer = referrer[referrer.find('/admin'):len(referrer)]
        key = 'key'+path.replace('/','_')
        if popup:
            key = 'popup'+path.replace('/','_')

        if path == referrer: #We are in same page as before
            if query_string == '': #Filter is empty, delete it
                if session.get(key,False):
                    del session[key]
                return None
            #            request.session[key] = query_string
            request.session[key] = request.GET.copy()
            request.session.modified = True
        else: #We are are coming from another page, restore filter if available
            if session.get(key, False):
            #                urllib.urlencode
                try:
                    query = request.session.get(key)
                    query.update(request.GET.copy())
                    query_string = urllib.urlencode(query)
                    redirect_to = path+'?' + query_string
                    request.session['redirected'] = True
                    return http.HttpResponseRedirect(redirect_to)
                except BaseException, e:
                    pass
                #                query_string=request.session.get(key)

        return None

class UMiddlewareSimplePage(object):
    def process_request(self, request, cls):
        try:
            if not hasattr(request, 'simple_page'):
                request.simple_page = None

            url =  re.sub(r'/+', '/', '/%s/' % request.path_info.strip('/'), re.IGNORECASE)
            sps = []
            #check_re

            #check if this seller subdomain
            qset = cls.site_objects.filter(url = url, state = True)

            for idx, sp in enumerate(qset):
                sps.append(sp)

            if len(sps):
                request.simple_page = sps
        except cls.DoesNotExist:
            request.simple_page = None