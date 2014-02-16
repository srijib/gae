#-*- coding: utf-8 -*-
#!/usr/bin/env python
import cgi
import cgitb
cgitb.enable()
print "so bad 2"
form = cgi.FieldStorage()
print form
from google.appengine.api import mail
mail.send_mail("lihaohua90@gmail.com", "13821254203@139.com", "主题", "正文")
print "mail sent"
print dir(form["dddd"])
print form["dddd"].name
print form["dddd"].value

print "end of so bad 2"
