from django.conf.urls.defaults import *
import models
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('users.views',
    (r'^sign_up/$', 'sign_up'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^(?P<user_id>\d+)/$', 'profile'),
    (r'^password_reset/$', 'password_reset'),
    (r'^account/$', 'account'),
    (r'^change_email/$', 'change_email'),
    (r'^change_password/$', 'change_password'),
)
