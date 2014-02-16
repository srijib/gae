# encoding: utf-8
import os
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello");
class ListHandler(webapp2.RequestHandler):
    def get(self):
        from google.appengine.api import users
        from google.appengine.ext.webapp import template
        from model import File
        current_user = users.get_current_user()
        template_values = {}
        query = File.gql('where author=:1 order by name', current_user)
        filelist = query.fetch(1000)
        for file in filelist:
            file.size = len(file.content)
        template_values['filelist'] = filelist
        template_values['logout_url'] = users.create_logout_url("")
        template_values['change_user_url'] = users.create_logout_url("list")
        template_values['nickname'] = users.get_current_user().nickname()
        self.response.out.write(template.render('templates/list.html', template_values))
class EditHandler(webapp2.RequestHandler):
    def get(self):
        from google.appengine.ext.webapp import template
        from model import File
        template_values = {}
        name = self.request.get('name')
        if not name:
            new_file = True
            import time
            template_values['defaultname'] = time.strftime("%Y%m%d%H%M%S.py")
        else:
            template_values['name'] = name
            query = File.gql('where name=:1', name)
            if query.count() > 0:
                new_file = False
                file_obj = query.fetch(1)[0]
                template_values['code'] = file_obj.content
            else:
                new_file = True
        if new_file:
            template_values['new_file'] = True
            with open('extra/script.tpl.py') as fp: template_values['code'] = fp.read()
        self.response.out.write(template.render('templates/edit.html', template_values))
class RunHandler(webapp2.RequestHandler):
    def runCode(self, code):
        import sys, cStringIO, traceback
        
        save_stdout = sys.stdout
        
        #import __builtin__
        #save_import = __builtin__.__import__
        #from dynamic_import import db_import
        #__builtin__.__import__ = db_import
        
        results_io = cStringIO.StringIO()
        try:
            sys.stdout = results_io
            code = code.replace("\r\n", "\n")
            try:
                compiled_code = compile(code, '<string>', 'exec')
                # exec(compiled_code, globals())
                # exec(compiled_code, globals(), locals())
                # 纠结中
                exec(compiled_code, locals())
            except Exception, e:
                traceback.print_exc(file=results_io)
        finally:
            sys.stdout = save_stdout
            #__builtin__.__import__ = save_import
        results = results_io.getvalue()
        return results
    def get(self):
        self.response.out.write("Run page request must be POST.")
    def post(self):
        code = self.request.get('code')
        results = self.runCode(code)
        self.response.out.write(results)
class RunFileHandler(RunHandler):
    def get(self):
        self.handleRunFile()
    def post(self):
        self.handleRunFile()
    def handleRunFile(self):
        from google.appengine.api import users
        current_user = users.get_current_user()
        name = self.request.get('name')
        from model import File
        query = File.gql("where name=:1 and author=:2", name, current_user)
        if query.count() <= 0:
            self.response.out.write(u'无法找到此文件或没有权限: %s' %name)
        else:
            file_obj = query.fetch(1)[0]
            code = file_obj.content
            results = self.runCode(code)
            self.response.out.write(results)
class SaveHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Save page request must be POST.")
    def post(self):
        from google.appengine.api import users
        from model import File
        code = self.request.get('code')
        name = self.request.get('name')
        current_user = users.get_current_user()
        query = File.gql("where name=:1 and author=:2", name, current_user)
        if query.count() > 0:
            file_obj = query.fetch(1)[0]
        else:
            from model import File
            file_obj = File(name=name, author = current_user)
        file_obj.content = code
        file_obj.put()
        self.response.out.write('保存成功')
class DeleteHandler(webapp2.RequestHandler):
    def handleDelete(self):
        from google.appengine.api import users
        from model import File
        name = self.request.get('name')
        current_user = users.get_current_user()
        query = File.gql("where name=:1 and author=:2", name, current_user)
        if query.count() > 0:
            file_obj = query.fetch(1)[0]
            file_obj.delete()
            return True
        else:
            return False
    def post(self):
        if self.handleDelete():
            self.response.out.write('删除成功')
        else:
            self.response.out.write('删除失败')
    def get(self):
        self.handleDelete()
        self.redirect('list')
class DownloadHandler(webapp2.RequestHandler):
    def get(self):
        from google.appengine.api import users
        from model import File
        import urllib
        current_user = users.get_current_user()
        name = self.request.get('name')
        query = File.gql("where name=:1 and author=:2", name, current_user)
        if query.count() > 0:
            file_obj = query.fetch(1)[0]
            self.response.headers['Content-Type'] = 'application/octet-stream'
            self.response.headers['Content-Disposition'] = 'attachment; filename=%s' %urllib.quote(file_obj.name.encode('utf-8'))
            self.response.out.write(file_obj.content)
            return
        else:
            self.response.out.write("文件不存在或没有权限.")
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/list', ListHandler),
    ('/edit', EditHandler),
    ('/save', SaveHandler),
    ('/run', RunHandler),
    ('/runfile', RunFileHandler),
    ('/delete', DeleteHandler),
    ('/download', DownloadHandler),
    ], debug=True)
