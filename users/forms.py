from django import forms
from django.contrib.auth.models import User
from recaptcha_works.fields import RecaptchaField


class UserField(forms.CharField):
    def clean(self, value):
        super(UserField, self).clean(value)
        try:
            User.objects.get(username=value)
            raise forms.ValidationError("Username is taken.")
        except User.DoesNotExist:
            return value


class SignUpForm(forms.Form):
    username = UserField(max_length=16)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat password")
    email = forms.EmailField(required=False)
    recaptcha = RecaptchaField(label='Human test', required=True)

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return self.data['password']

    def clean(self,*args, **kwargs):
        self.clean_password()
        return super(SignUpForm, self).clean(*args, **kwargs)


class LoginForm(forms.Form):
    username = forms.CharField(initial="username")
    password = forms.CharField(initial="password", widget=forms.PasswordInput())

class PasswordResetForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    recaptcha = RecaptchaField(label='Human test', required=True)

    def clean_email(self):
        if not User.objects.filter(username=self.data['username'],
                                   email=self.data['email']):
            raise forms.ValidationError('Email doesn\'t match username.')
        return self.data['email']

    def clean(self,*args, **kwargs):
        self.clean_email()
        return super(PasswordResetForm, self).clean(*args, **kwargs)

class EditEmailForm(forms.Form):
    email = forms.EmailField()

class EditPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat password")

    def __init__(self,user,post=None):
        super(EditPasswordForm, self).__init__(post)
        self.user = user

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return self.data['password']


    def clean_current_password(self):
        if not self.user.check_password(self.data['current_password']):
            raise forms.ValidationError('Incorrect password.')
        return self.data['password']

    def clean(self,*args, **kwargs):
        self.clean_password()
        self.clean_current_password()
        return super(EditPasswordForm, self).clean(*args, **kwargs)



