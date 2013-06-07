# In the following example, only the email field will be visible (the
# HoneypotFields are named as such to increase the chance that a bot
# will try to fill them in):
#
# class EmailForm(Form):
#    name = HoneypotField()
#    website = HoneypotField(initial='leave me')
#    email = EmailField()

from django.forms import *

EMPTY_VALUES = (None, '')

class HoneypotWidget(TextInput):
    is_hidden = True
    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment
        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)
        if not self.attrs.has_key('class'):
            self.attrs['style'] = 'display:none'
    def render(self, *args, **kwargs):
        value = super(HoneypotWidget, self).render(*args, **kwargs)
        if self.html_comment:
            value = '<!-- %s -->' % value
        return value

class HoneypotField(Field):
    widget = HoneypotWidget
    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value
        raise ValidationError('Anti-spam field changed in value.')

