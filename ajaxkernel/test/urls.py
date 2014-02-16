from django.conf.urls.defaults import *

urlpatterns = patterns('test.views',
    (r'^$', 'index'),
    (r'^weather/?$', 'weather'),
    (r'^qiubai/?$', 'qiubai'),
)
