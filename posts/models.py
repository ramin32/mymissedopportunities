from django.db import models
from string import capitalize
from django.contrib.auth.models import User
from datetime import datetime


CATEGORY_CHOICES = ['dating','school', 'work','friendship','family','other']

labeled_choices=[(c,capitalize(c)) for c in CATEGORY_CHOICES]
    
def get_username(model):
    if model.user:
        return model.user.username
    return model.nick

class Post(models.Model):
    category = models.CharField(max_length=10, choices=labeled_choices)
    missed_opportunity = models.CharField(max_length=500)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)

    date_created = models.DateTimeField(default=datetime.now, editable=False)
    is_spam = models.BooleanField(editable=False)

    user = models.ForeignKey(User, editable=False, blank=True, null=True)
    nick = models.CharField(max_length=16, blank=True, null=True)

    def get_username(self):
        return get_username(self)

    def __unicode__(self):
        return "%s: %s" % (self.get_username(), self.missed_opportunity)

    class Meta:
        ordering = ['-date_created']


class Comment(models.Model):
    comment = models.CharField(max_length=500)

    date_created = models.DateTimeField(default=datetime.now, editable=False)
    is_spam = models.BooleanField(editable=False)

    user = models.ForeignKey(User, editable=False, blank=True, null=True)
    nick = models.CharField(max_length=16, blank=True, null=True)

    post = models.ForeignKey(Post, editable=False)

    def get_username(self):
        return get_username(self)

    def __unicode__(self):
        return "%s: %s" % (self.get_username(), self.comment)

    class Meta:
        ordering = ['-date_created']

