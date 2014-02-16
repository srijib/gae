# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from google.appengine.ext import deferred
from lib.feed.QiubaiFeedParser import QiubaiFeedParser
from lib.sender.FetionRPC import sendFetionMessageIgnoreFailure
from lib.weather.WeatherParser import WeatherParser
def index(request):
    return direct_to_template(request, 'test/index.html', {})
def qiubai(request):
    msg = QiubaiFeedParser().getString()
    deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "13821254203", msg)
    # deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "13920510408", msg) # 老婆
    # deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "15828514324", msg) # 孙佳维
    # deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "13761318157", msg) # 娄林
    # deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "15121036802", msg) # 刘仁瑞
    return render_to_response("test/weather.html", {'msg':msg})
def weather(request):
    msg = WeatherParser.getReportString(u'天津市河东区')
    deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "13821254203", msg)
    # deferred.defer(sendFetionMessageIgnoreFailure, "13821254203", "snowmanshan0913", "13472620670", msg) #龚正
    # deferred.defer(sendFetionMessage, "13821254203", "snowmanshan0913", "15121025917", msg) # 高威
    return render_to_response("test/weather.html", {'msg':msg})
