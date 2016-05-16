from django.contrib.auth.models import Group
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proff.settings")

from django.contrib.admin.sites import AdminSite
from django.utils.importlib import import_module

import logging
logger = logging.getLogger('proff')


class SuperAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_superuser and request.user.is_active and request.user.is_staff

def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()

def autodiscover(admin, **kwargs):
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        try:
            module = import_module('.admin', app)
            module.admin_register(admin)
        except AttributeError, e:
            logger.debug('cant import fn')

        except ImportError, e:
            logger.debug('cant find admin module %s' % app)

