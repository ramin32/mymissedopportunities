# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import list_detail
from django.template import RequestContext
from django.views.generic.list_detail import object_detail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from mymissedopportunities.posts.forms import *
from mymissedopportunities.posts.models import *
from mymissedopportunities.util import json_http, spam
from mymissedopportunities.users.forms import *


sort_type_mapping = {'best': '-up_votes', 'worst':'-down_votes'}
@csrf_protect
def posts(request, page=0, category=None, sort_type=None, flash=None):

    if request.user.is_authenticated():
        post_form = PostForm()
        comment_form = CommentForm()
    else:
        post_form = AnonymousPostForm()
        comment_form = AnonymousCommentForm()

    if category:
        post_list = Post.objects.filter(category=category)
        post_form.fields['category'].initial=category
    else:
        post_list = Post.objects.all()

    if sort_type:
        post_list = post_list.order_by(sort_type_mapping[sort_type])

    post_list = post_list.exclude(is_spam=True)

    return render_to_response('posts/posts.html',
                              {'post_list': post_list, 
                               'post_form': post_form,
                               'comment_form': comment_form,
                               'login_form': LoginForm(),
                               'flash': flash},
                               context_instance=RequestContext(request))

@csrf_protect
def submit_post(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            form = PostForm(request.POST)
        else:
            form = AnonymousPostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated():
                post.user = request.user
            post.is_spam = spam.is_spam(request, post.missed_opportunity, post.get_username())
            post.save()

            if post.is_spam:
                return json_http.render_to_json_response('spam.html', {'is_post': True})

            return json_http.render_to_json_response('posts/post.html', 
                                                    {'post': post, 'comment_form': CommentForm()}, 
                                                    context_instance=RequestContext(request))
        

        return json_http.render_to_json_response('form.html', 
                {'form': form}, 
                status="failure", 
                context_instance=RequestContext(request))
    else:
        return HttpResponse(status=400)

@csrf_protect
def add_comment(request, post_id):
    if request.is_ajax():
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
        else:
            form = AnonymousCommentForm(request.POST)

        if form.is_valid():
            post = get_object_or_404(Post, pk=int(post_id))
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated():
                comment.user = request.user
            comment.is_spam =  spam.is_spam(request, comment.comment, comment.get_username())
            comment.save()
            if comment.is_spam:
                return json_http.render_to_json_response('spam.html', {'is_post': False})
            
            return json_http.render_to_json_response('posts/comment.html', {'comment': comment}, context_instance=RequestContext(request))
        else:
            return json_http.render_to_json_response('form.html', {'form': form}, status="failure", context_instance=RequestContext(request))
    else:
        return HttpResponse(status=400)

    
@csrf_protect
def add_vote(request, post_id, vote_type):
    if request.is_ajax():
        post = get_object_or_404(Post, pk=int(post_id))
        old_val = getattr(post, vote_type)
        setattr(post, vote_type, old_val+1)
        post.save()
        return HttpResponse('')
    else:
        return HttpResponse(status=400)

 
