# -*- coding: utf-8 -*-
from django import forms
from guestbook.models import Greeting

TOPIC_CHOICES = (
    ('google weather report', '谷歌天气预报'),
    ('qiushibaike', '糗事百科每日Top10'),
    ('cnbeta', 'cnBeta.COM'),
)
class ChoicesForm(forms.Form):
    # choices = forms.ChoiceField(choices=TOPIC_CHOICES)
    choices = forms.MultipleChoiceField( choices=TOPIC_CHOICES, widget=forms.CheckboxSelectMultiple())
    # choice = forms.CheckboxInput()