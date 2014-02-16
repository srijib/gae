from django.conf.urls.defaults import *
from django.contrib.auth.forms import AuthenticationForm

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    # Example:
    # (r'^ajaxkernel/', include('ajaxkernel.app.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    # (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/index/', }),
    # (r'^$', 'index.views.index'),

    # index
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/index/', }),
    (r'^index$', 'django.views.generic.simple.redirect_to', {'url': '/index/', }),
    (r'^index/', include('index.urls')),
    
    (r'^test$', 'django.views.generic.simple.redirect_to', {'url': '/test/', }),
    (r'^test/', include('test.urls')),

    # guestbook
    (r'^guestbook$', 'django.views.generic.simple.redirect_to', {'url': '/guestbook/', }),
    (r'^guestbook/', include('guestbook.urls')),

    # my home
    (r'^my$', 'django.views.generic.simple.redirect_to', {'url': '/my/', }),
    (r'^my/', include('my.urls')),

    (r'^accounts/create_user/$', 'guestbook.views.create_new_user'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'guestbook/login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/guestbook/',}),
)
