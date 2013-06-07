from django.conf.urls.defaults import *
import models
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

categories = '|'.join(models.CATEGORY_CHOICES)

urlpatterns = patterns('posts.views',
    (r'^(?P<category>%s)/$' % categories, 'posts'),
    (r'^(?P<sort_type>best|worst)/$', 'posts'),
    (r'^submit_post/$', 'submit_post'),
    (r'^(?P<post_id>\w+)/(?P<vote_type>up_votes|down_votes)/add/$','add_vote'),
    (r'^(?P<post_id>\w+)/comment/$','add_comment'),
)
