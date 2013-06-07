from django.db import models
from datetime import datetime

class Feedback(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    comment = models.CharField(max_length=500)
    date_created = models.DateTimeField(default=datetime.now, editable=False)
    is_spam = models.BooleanField(editable=False)
    
    class Meta:
        ordering = ['-date_created']

