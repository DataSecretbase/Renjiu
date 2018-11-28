from django.shortcuts import render
from django.template import Context, Template
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from .email_template import joinus as joinusus
# Create your views here.

def joinus(request):
    join_info = {}
    join_info['cpname'] = request.GET.get('cpname')
    join_info['project'] = request.GET.get('project')
    join_info['nickname'] = request.GET.get('nickname')
    join_info['phone'] = request.GET.get('phone')
    join_info['content'] = request.GET.get('content')
    join_info['datetime'] = datetime.now()
    t = Template(joinusus.T)
    c = Context({'join_info':join_info})
    
    send_mail('标题','内容',settings.EMAIL_FROM,
              ['2175666031@qq.com'],
              html_message = t.render(c),
              fail_silently=False)
    return HttpResponse('ok')
