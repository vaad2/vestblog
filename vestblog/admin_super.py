from django.contrib.admin.sites import AdminSite
from frontend.admin import admin_register
from common.admin import autodiscover


class SuperAdminSite(AdminSite):
    def has_permission(self, request):
        # return request.user.is_superuser and request.user.is_active and request.user.is_staff
        return request.user.is_active and request.user.is_staff


admin_super = SuperAdminSite(name='admin_super')
autodiscover(admin_super)

