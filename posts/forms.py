from django.forms import Textarea, CharField, ModelForm, CharField
from django.utils.translation import ugettext_lazy as _
from models import *

class PostForm(ModelForm):
    missed_opportunity = CharField(
           error_messages={'min_length': u'Your message is too short.',
                           'max_length': u'Your message is too long.',
                           'required': u'This field is required.'},
            min_length=15, 
            max_length=500,
            widget=Textarea(attrs={'cols': 82, 'rows': 4})
    )
    class Meta:
        model = Post
        fields = ('category', 'missed_opportunity')

class AnonymousPostForm(PostForm):
    nick = CharField(initial='Anonymous', max_length=16)
    class Meta(PostForm.Meta):
        fields = ('category', 'missed_opportunity', 'nick')

    
class CommentForm(ModelForm):
    class Meta:
        model = Comment       
        widgets = {'comment': Textarea(attrs={'cols': 82, 'rows': 3})}
        fields = ('comment')

class AnonymousCommentForm(CommentForm):
    nick = CharField(initial='Anonymous', max_length=16)

    class Meta(CommentForm.Meta):
        fields = ('comment', 'nick')

