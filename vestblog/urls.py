from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from filebrowser.sites import site

from . import admin_super, admin_client

urlpatterns = patterns('',
                        (r'^grappelli/', include('grappelli.urls')),

                        url(r'^admin/filebrowser/', include(site.urls)),
                        url(r'^admin/', include(admin_super.admin_super.urls)),

                        url(r'^', include('frontend.urls', namespace='frontend')),

)