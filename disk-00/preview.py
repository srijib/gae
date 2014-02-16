# -*- coding: utf-8 -*-
#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *
from lib import MyHandler
import ADDRESS

class PdfPreviewHandler(MyHandler):
    def get(self):
        key = self.request.get("key")
        if not key:
            return
        file = File.get(db.Key(key))
        if not file:
            self.response.out.write("File not Found. Maybe it has been removed.")
            return 
        import mimetypes
        mime = mimetypes.guess_type(file.filename)
        mime = mime[0] or "application/octet-stream"
        if not "pdf" in mime:
            self.response.out.write("It's not a pdf file.")
            self.response.set_status(400)
            return
        from lib import pdf2txt
        from cStringIO import StringIO
        fp = StringIO()
        node = file.head.next
        while node:
            fp.write(node.data)
            node = node.next
        startpage = self.request.get("startpage")
        endpage = self.request.get("endpage")
        if startpage and endpage:
            try:
                startpage = int(startpage)
                endpage = int(endpage)
                if(startpage > endpage):
                    startpage, endpage = endpage, startpage
            except:
                startpage = endpage = 0
        else:
            startpage = endpage = 0
        from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
        try:
            if startpage == 0 and endpage == 0:
                out_text = pdf2txt(fp)
            else:
                pagenos = range(startpage-1, endpage)
                out_text = pdf2txt(fp, pagenos)
        except PDFTextExtractionNotAllowed:
            self.response.out.write("Parse error: Pdf file may be protected.")
            return
        except:
            self.response.out.write("Exception.")
            return
        import cgi
        out_text = cgi.escape("\n".join([l for l in out_text.split("\n") if l.strip()])).replace("\n","<br>\n").replace(" ","&nbsp;")
        
        self.response.out.write(u"""<h4>预览: %s</h4>""" %file.filename)
        if startpage==0 and endpage==0:
            self.response.out.write(u"""<p>全部页</p>""" %startpage)
        elif startpage==endpage:
            self.response.out.write(u"""<p>第%d页</p>""" %startpage)
        else :
            self.response.out.write(u"""<p>第%d页 到 第%d页</p>""" %(startpage, endpage))
        self.response.out.write(u"""
<form action="/pdfpreview" method="get"><input name="key" type="hidden" value="%s">
跳转: 第<input name="startpage" style="width:35px" type="text" value="%d">页 到 第<input style="width:35px" name="endpage" type="text" value="%d">页 <input type="submit" value="查看"></form><br>
""" %(file.key(), startpage, endpage))
        self.response.out.write(out_text.decode("utf8"))
def main():
    application = webapp.WSGIApplication([('/pdfpreview', PdfPreviewHandler), ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
