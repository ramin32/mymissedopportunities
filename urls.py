from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^$', 'posts.views.posts'),
    (r'^posts/', include('mymissedopportunities.posts.urls')),
    (r'^feedback/', include('mymissedopportunities.feedback.urls')),
    (r'^users/', include('mymissedopportunities.users.urls')),
)

urlpatterns += patterns('django.views.generic',
    (r'^about/$', 'simple.direct_to_template', {'template': 'about.html'}),
    (r'^terms/$', 'simple.direct_to_template', {'template': 'terms.html'}),
)
