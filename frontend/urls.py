from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       # url(r'^([A-Za-z]{2}/)?$', views.IndexView.as_view(), name='IndexView'),
                       # url(r'^([A-Za-z]{2}/)?article/(?P<slug>[^\/]+)/$', views.ArticleDetail.as_view(), name='ArticleDetail')
                       url(r'^$', views.IndexView.as_view(), name='IndexView'),
                       url(r'^article/(?P<slug>[^\/]+)/$', views.ArticleDetail.as_view(), name='ArticleDetail'),
                       url(r'^category/(?P<slug>[^\/]+)/$', views.CategoryArticleList.as_view(), name='CategoryArticleList'),
                       url(r'^tag/(?P<slug>[^\/]+)/$', views.TagArticleList.as_view(), name='TagArticleList')

)
