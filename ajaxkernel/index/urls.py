from django.conf.urls.defaults import *

urlpatterns = patterns('index.views',
    (r'^$', 'index'),
    (r'^subscribe/?$', 'subscribe'),
    (r'^send_mail/?$', 'send_mail'),
)
