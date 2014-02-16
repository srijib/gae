# -*- coding: utf-8 -*-
import django
from django.views.generic.simple import direct_to_template
from index.forms import ChoicesForm

def index(request, *args):
    form = ChoicesForm(auto_id=False)
    # return direct_to_template(request, 'index/index.html', {'form': form})
    return direct_to_template(request, 'index/test.html', {'form': form})
def subscribe(request):
    return direct_to_template(request, 'index/subscribe.html', {})
def send_mail(request):
    django.core.mail.send_mail("subject", "body", "cloudriveservice@gmail.com", ["eggfly@qq.com"])
    return django.views.generic.simple.HttpResponse("ok")