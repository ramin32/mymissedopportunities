from models import Feedback
from recaptcha_works.fields import RecaptchaField
from django.forms import ModelForm, Textarea

class FeedbackForm(ModelForm):
    recaptcha = RecaptchaField(label='Human test', required=True)
    class Meta:
        model = Feedback       
        widgets = {'comment': Textarea(attrs={'cols': 52, 'rows': 5})}

