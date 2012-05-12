from django.conf.urls.defaults import patterns, include, url
#from mainpage import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boom2_0.views.home', name='home'),
    # url(r'^boom2_0/', include('boom2_0.foo.urls')),
    url(r'^$', 'apps.mainpage.views.main', name="home"),
	url(r'^category/(?P<slug>[-\w]+)$', 'apps.mainpage.views.category', name='category'),
    url(r'^seller/(?P<slug>[-\w]+)$', 'apps.mainpage.views.seller',name="seller"),

	url(r'^user/login/$', 'apps.users.views.login', name='login'),
	url(r'^user/register/$', 'apps.users.views.register', name='register'),
	url(r'^user/confirm/(?P<activation_key>[-\w\d]+)$', 'apps.users.views.confirm', name='confirm'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
