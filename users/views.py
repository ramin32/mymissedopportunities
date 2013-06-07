# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render_to_response, get_object_or_404
from forms import * 
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.template.loader import render_to_string
from recaptcha_works.decorators import fix_recaptcha_remote_ip
from mymissedopportunities.posts.models import *
from mymissedopportunities.posts.forms import *
from mymissedopportunities.users.forms import *
from django.core.mail import send_mail
import mymissedopportunities
import string
from random import choice

def email_confirmation(user):
    message = render_to_string('users/sign_up_email.html', {'user':user})
    user.email_user('Welcome to MyMissedOpportunities.com', message)

@csrf_protect
@fix_recaptcha_remote_ip
def sign_up(request):
    if request.method == 'GET':
        return render_to_response('users/sign_up_form.html', {'sign_up_form':SignUpForm(), 'login_form': LoginForm()}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], 
                                     form.cleaned_data['email'],
                                     form.cleaned_data['password'])
            email_confirmation(user)

            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
            auth.login(request, user)
            return render_to_response('users/sign_up_success.html', context_instance=RequestContext(request))

        else:
            return render_to_response('users/sign_up_form.html', {'sign_up_form':form, 'login_form': LoginForm()}, context_instance=RequestContext(request))

@csrf_protect
def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = auth.authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:
            if user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('users/account_disabled.html', context_instance=RequestContext(request))
    post_list = Post.objects.all()
    return render_to_response('posts/posts.html',
                              {'post_list': post_list, 
                               'post_form': PostForm(),
                               'comment_form': CommentForm(),
                               'login_form': form,
                               'login_error':"Incorrect Password"},
                               context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

        
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    c = {
        'post_list': Post.objects.filter(user=user),
        'comment_post_list': Post.objects.filter(comment__user=user),
        'user': user

    }
    return render_to_response('users/profile.html', c, context_instance=RequestContext(request))

def generate_password(length=10, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

def email_password_reset(user, password):
    message = render_to_string('users/password_reset_email.html', {'password': password})
    user.email_user('MyMissedOpportunities.com: password reset', message)

@csrf_protect
@fix_recaptcha_remote_ip
def password_reset(request):
    if request.method == 'GET':
        form = PasswordResetForm()
        return render_to_response('users/password_reset.html', 
            {'password_reset_form': form}, 
            context_instance=RequestContext(request))

    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = generate_password()
            user = User.objects.filter(username=form.cleaned_data['username'],
                                   email=form.cleaned_data['email'])[0]
            user.set_password(new_password)
            user.save()
            email_password_reset(user, new_password)
            return render_to_response('users/password_reset_sent.html', context_instance=RequestContext(request))
        else:
            return render_to_response('users/password_reset.html', 
                {'password_reset_form': form}, 
                context_instance=RequestContext(request))

@csrf_protect
def account(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            email_form = EditEmailForm()
            email_form.fields['email'].initial = request.user.email
            return render_to_response('users/account.html',
                {'user':request.user,
                 'email_form': email_form,
                 'password_form': EditPasswordForm(request.user)},
                context_instance=RequestContext(request))
    return HttpResponseNotFound()

def change_email(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            email_form = EditEmailForm(request.POST)
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['email']
                request.user.save()
                return HttpResponseRedirect('/users/account/')
            return render_to_response('users/account.html',
                {'user':request.user,
                 'email_form': email_form,
                 'password_form': EditPasswordForm(request.user)},
                context_instance=RequestContext(request))
    return HttpResponseNotFound()

def change_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            email_form = EditEmailForm()
            email_form.fields['email'].initial = request.user.email
            password_form = EditPasswordForm(request.user, request.POST)
            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data['password'])
                request.user.save()
                return HttpResponseRedirect('/users/account/')
            else:
                return render_to_response('users/account.html',
                                          {'user':request.user,
                                           'email_form': email_form,
                                           'password_form': password_form},
                                           context_instance=RequestContext(request))
    return HttpResponseNotFound()

