from django.contrib.sites.models import Site

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_request():
    """ returns the request object for this thead """
    return getattr(_thread_locals, "request", None)

def get_current_site():
    request = get_current_request()
    try:
        from django.conf import settings
        site = Site.objects.get(pk = settings.SITE_ID)
    except BaseException, e:
        site = None
    if request:
        from urlparse import urlparse
        domain = urlparse(request.get_host())[2]
        try:
            site = Site.objects.get(domain = domain)
        except BaseException, e:
            pass

    return site

def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request and hasattr(request, 'user') and request.user.is_authenticated():
        return request.user
    return None

def set_thread_var(name, value):
    setattr(_thread_locals, name, value)

def get_thread_var(name, default = None):
    return getattr(_thread_locals, name, default)

