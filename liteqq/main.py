from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch

headers = {"Connection": "close"}
host = 'http://kconn.tencent.com:21001'
max_try = 8
def to_dict(info):
	info = info.split('&')
	d_info = {}
	for i in info:
		item = i.split('=')
		try:
			d_info[item[0].upper()]=item[1]
		except:
			d_info[item[0].upper()]=''
	return d_info

class MainHandler(webapp.RequestHandler):
	def redirect(self, host):
		global headers, max_try
		params =	"VER=%s&CMD=Login&SEQ=%d&UIN=%s&PS=%s&M5=1&LC=B58D4DF7758A47E7&CKE=0" %(self.ver, self.seq, self.qq, self.pwd_hex)
		result = None
		for i in range(max_try):
			try:
				result = urlfetch.fetch(
					url=host,
					payload = params,
					headers = headers,
					method = urlfetch.POST,
				)
				self.seq+=1	
				break
			except:
				continue
		return result

	def login(self):
		global headers, max_try
		params =  "VER=%s&CMD=Login&SEQ=%d&UIN=%s&PS=%s&M5=1&LC=B58D4DF7758A47E7&CKE=0"%(self.ver, self.seq, self.qq, self.pwd_hex)
		result = None
		for i in range(max_try):
			try:
				result = urlfetch.fetch(
					url=self.ip,
					payload = params,
					headers = headers,
					method = urlfetch.POST,
				)
				self.seq+=1	
				break
			except:
				continue
		return result

	def get(self):
		global host
		self.seq = 100
		self.ver = '1.3'
		self.qq = 329677581
		self.pwd_hex = '8065265E5BDF214E2F012D6CAE57FEA1'
		self.response.out.write(u'''<html>QQ Main<br/>''')
		'''result = self.redirect(host)
		self.response.out.write(result.content)
		self.response.out.write("<br/>")
		result = to_dict(result.content)'''
		#self.ip ="http://%s:%s"%(result['SI'], result['SP'])
		self.ip ="http://119.147.10.11:14000"
		result = self.login()
		self.response.out.write(result.content)
		self.response.out.write("<br/>")
		self.response.out.write(u"""<br></html>""")

def main():
	application = webapp.WSGIApplication([('/.*', MainHandler)],
																			 debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
