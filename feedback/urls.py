from django.conf.urls.defaults import *
import models
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('feedback.views',
    (r'^submit_feedback', 'submit_feedback'),
)
