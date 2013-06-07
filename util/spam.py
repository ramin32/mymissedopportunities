import akismet
from django.conf import settings
from recaptcha.client import captcha

spam_api = akismet.Akismet(agent="mymissedopportunities")

def is_spam(request, message, author):
    data = {
        'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'referrer': request.META.get('HTTP_REFERER', ''),
        'comment_type': 'comment',
        'comment_author': author,
    }
    return spam_api.comment_check(message, data)

def verify_captcha(request):
    return captcha.submit(request.POST['recaptcha_challenge_field'],
                          request.POST['recaptcha_response_field'],
                          settings.RECAPTCHA_PRIVATE_KEY,
                          request.META['REMOTE_ADDR']).is_valid

