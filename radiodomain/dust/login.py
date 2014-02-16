import Cookie,urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch

form_email = 'lhh1990@gmail.com'
form_password = 'hiradio'

cookie_buf = Cookie.SimpleCookie();

def make_cookie_header(cookie):
  ret = ''
  for v in cookie.values():
    ret += '%s=%s;' % (v.key, v.value)
  return ret

def do_redirect(url, cookie, referer):
  result = urlfetch.fetch(
    url=url,
    headers={
      'Cookie':make_cookie_header(cookie),
      'Content-Type': 'application/x-www-form-urlencoded',
      'Referer': referer
    },
    method=urlfetch.GET,
    follow_redirects = False,
  )
  return result

def login():
  verify_url = 'http://www.douban.com/login'
  verify_data= urllib.urlencode(
    {
    'form_email':  form_email,
    'form_password': form_password,
    })
  result = urlfetch.fetch(
    url=verify_url,
    headers={'Cookie':make_cookie_header(cookie_buf),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.douban.com/login?type=simple&redir=%2Fservice%2Faccount%2F%3Freturn_to%3Dhttp%253A%252F%252Fdouban.fm%252Fradio%26sig%3D8f0d03ca71%26mode%3Dcheckid_setup'},
    method=urlfetch.POST,
    payload=verify_data,
    follow_redirects = False,
    )
  return result

def get_data(cookie):
  status_url = 'http://douban.fm/j/mine/playlist'

  result = urlfetch.fetch(
    url=status_url,
    headers={
      'Cookie':make_cookie_header(cookie),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    method=urlfetch.GET
  )
  return result
class MainPage(webapp.RequestHandler):
  def get(self):
    global cookie_buf
    #login
    result = login()
    
    cookie_buf = Cookie.SimpleCookie(result.headers.get('set-cookie', '')) #1st time need cookie
    callback_url = result.headers.get('location','xx')
    result = do_redirect(callback_url, cookie_buf,"http://www.douban.com/login?type=simple&redir=%2Fservice%2Faccount%2F%3Freturn_to%3Dhttp%253A%252F%252Fdouban.fm%252Fradio%26sig%3D8f0d03ca71%26mode%3Dcheckid_setup")
    
    callback_url = result.headers.get('location','xx')
    result = do_redirect(callback_url, cookie_buf, "http://www.douban.com/login?type=simple&redir=%2Fservice%2Faccount%2F%3Freturn_to%3Dhttp%253A%252F%252Fdouban.fm%252Fradio%26sig%3D8f0d03ca71%26mode%3Dcheckid_setup")
    
    callback_url = result.headers.get('location','xx')
    cookie_buf = Cookie.SimpleCookie(result.headers.get('set-cookie', ''))
    result = get_data(cookie_buf)
    
    self.response.out.write(result.content)

def main():
  application = webapp.WSGIApplication([('/.*', MainPage)],
                                       debug=True)
  util.run_wsgi_app(application)
if __name__ == '__main__':
  main()