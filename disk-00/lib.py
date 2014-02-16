#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os
class MyHandler(webapp.RequestHandler):
    def render(self, template_file, template_value):
        path = os.path.join(os.path.dirname(__file__), template_file)
        self.response.out.write(template.render(path, template_value))

def pdf2txt(fp, pagenos = set()):
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.converter import TextConverter
    from pdfminer.pdfinterp import PDFResourceManager, process_pdf
    from pdfminer.layout import LAParams
    from cStringIO import StringIO
    outfp = StringIO()
    laparams = LAParams()
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, outfp, codec="utf-8", laparams=laparams)
    process_pdf(rsrcmgr, device, fp, pagenos)
    device.close()
    out_text = outfp.getvalue()
    outfp.close()
    return out_text
    
