from django.template.loader import render_to_string
from django.http import HttpResponse
import json

def render_to_json_response(template, context, status='success', context_instance=None):
    html = render_to_string(template, context, context_instance)
    json_dict = {'html': html, 'status':status}
    json_response = json.dumps(json_dict)
    return HttpResponse(json_response)
