from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authBack.views.home', name='home'),
    url(r'^$', direct_to_template, {'template' : 'index.html'}),
    url(r'^generate$', 'authBackend.views.generate'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
     (r'^facebook/login/$', 'facebook.views.login_fb'),
     (r'^facebook/post$', 'facebook.views.post_to_wall'),
     (r'^facebook/authentication_callback/$', 'facebook.views.authentication_callback'),
     
    (r'^account/', include('django.contrib.auth.urls')),
)

urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'static'}
    ))