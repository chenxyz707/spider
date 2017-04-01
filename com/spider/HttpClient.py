# -*- coding: utf-8 -*-
import cookielib, urllib, urllib2, socket
import zlib,StringIO
class HttpClient:
  __cookie = cookielib.CookieJar()
  __proxy_handler = urllib2.ProxyHandler({"http" : '111.13.2.131:80'})
  __req = urllib2.build_opener(urllib2.HTTPCookieProcessor(__cookie),__proxy_handler)
  __req.addheaders = [
    ('Accept', 'application/javascript, */*;q=0.8'),
    ('User-Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)')
  ]
  urllib2.install_opener(__req)

  def Get(self, url, refer=None):
    try:
      req = urllib2.Request(url)
      req.add_header('Accept-encoding', 'gzip')
      if not (refer is None):
        req.add_header('Referer', refer)
      response = urllib2.urlopen(req, timeout=1200)
      html = response.read()
      gzipped = response.headers.get('Content-Encoding')
      if gzipped:
          html = zlib.decompress(html, 16+zlib.MAX_WBITS)
      return html
    except urllib2.HTTPError, e:
      return e.read()
    except socket.timeout, e:
      return ''
    except socket.error, e:
      return ''

  def Post(self, url, data, refer=None):
    try:
      #req = urllib2.Request(url, urllib.urlencode(data))
      req = urllib2.Request(url,data)
      if not (refer is None):
        req.add_header('Referer', refer)
      return urllib2.urlopen(req, timeout=120).read()
    except urllib2.HTTPError, e:
      return e.read()
    except socket.timeout, e:
      return ''
    except socket.error, e:
      return ''

  def Download(self, url, file):
    output = open(file, 'wb')
    output.write(urllib2.urlopen(url).read())
    output.close()

#  def urlencode(self, data):
#    return urllib.quote(data)

  def getCookie(self, key):
    for c in self.__cookie:
      if c.name == key:
        return c.value
    return ''

  def setCookie(self, key, val, domain):
    ck = cookielib.Cookie(version=0, name=key, value=val, port=None, port_specified=False, domain=domain, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    self.__cookie.set_cookie(ck)
#self.__cookie.clear() clean cookie
# vim : tabstop=2 shiftwidth=2 softtabstop=2 expandtab

HttpClient