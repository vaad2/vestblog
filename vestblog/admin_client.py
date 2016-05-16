from django.contrib.admin.sites import AdminSite


class AdminSiteClient(AdminSite):
    def has_permission(self, request):
        return request.user.groups.filter(name='clients').count() and request.user.is_active and request.user.is_staff


admin_client = AdminSiteClient(name='admin_client')
