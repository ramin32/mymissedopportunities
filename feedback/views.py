from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, loader, Context

from forms import FeedbackForm
from mymissedopportunities.util import spam
from recaptcha_works.decorators import fix_recaptcha_remote_ip

@csrf_protect
@fix_recaptcha_remote_ip
def submit_feedback(request):
    if request.method == 'GET':
        return render_to_response('feedback/feedback_form.html', 
            {'form': FeedbackForm()},
            context_instance=RequestContext(request))

    elif request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.is_spam = spam.is_spam(request, feedback.name, feedback.comment)
            feedback.save()
            return render_to_response('feedback/feedback_success.html',context_instance=RequestContext(request))

        return render_to_response('feedback/feedback_form.html',
                {'form':form},
                context_instance=RequestContext(request))
            


