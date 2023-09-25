#!/bin/env python3

import requests, os, sys
from http import cookies

# common library

APPLICATION = 'radius'
VERSION = '0.1'
SOURCE = 'https://github.com/underground-software/radius'
ROOT = '/var/orbit/kdlp.underground.software'
AUTH_SERVER = 'http://127.0.0.1:9092'

# shortand for bytes(string, "UTF-8")
def bytes8(string):
	return bytes(string, "UTF-8")

# shortand for str(string, "UTF-8")
def str8(string):
	return str(string, "UTF-8")

def DEBUG(strg):
    print(strg, file=sys.stderr)

def get_token_from_cookie(env):
    # get auth=$TOKEN from user cookie
    cookie_user_raw = env.get('HTTP_COOKIE', '')
    cookie_user = cookies.BaseCookie('')
    cookie_user.load(cookie_user_raw)

    auth = cookie_user.get('auth', cookies.Morsel())
    if auth.value is not None:
        return auth.value

def get_authorized_user(server, env):
    token = get_token_from_cookie(env)
    uri ='%s/check?token=%s' % (AUTH_SERVER, token)

    res = requests.get(uri, verify=False)

    DEBUG('req to uri="%s" returned %s' % (uri, res.status_code))
    DEBUG('content: %s' % res.text)
    
    if res.status_code == 200:
        return res.text

    return None

def appver():
    return "%s %s %s" % (APPLICATION, VERSION, SOURCE)

def messageblock(lst):
    res=''
    sep = '<br /><hr /><br />'

    res += sep
    for item in lst:
        res += "<code>%s = %s</code><br />" % (item[0], str(item[1]))
    res += sep

    return res

def h(v, c):
    return '<h%d>%s</h%d>' % (v, c, v)

def h1(c):
    return h(1, c)

def h2(c):
    return h(2, c)

def h3(c):
    return h(2, c)

def t_i(i):
    return ''.join(['\t' for x in range(i)])

def o(i, c):
    return '%s%s\n' % (t_i(i), c)

def ooo(i, c, d, e, j=0):
    return '%s%s%s' % (o(i, c), o(i+j, d), o(i, e))

def oOo(i, c, d, e):
    return ooo(i, c, d, e, j=1)

def oxo(i, c, d, e):
    return '%s%s%s' % (o(i, c), d, o(i, e))

def table_data(c, h=False, i=0):
    d = 'd'
    if h:
        d = 'h'
    a, b = '<t%s>' % d, '</t%s>' % d
    return oOo(i, a, c, b)

def table_row(c, h=False, i=0):
    d = ''.join([table_data(d, h=h, i=i+1) for d in c])
    return oxo(i, '<tr>', d, '</tr>')

def table(c, i=0):
    t=''
    h=True
    for r in c:
        t += table_row(r, h, i=i+1)
        h=False
    return oxo(i, '<table>', t, '</table>')

def button(c, i=0, a=''):
    return oOo(i, '<button %s>' % a, c, '</button>')

def ok_html(doc, SR, extra_docs=[], extra_headers=[]):
	SR('200 OK', [('Content-Type', 'text/html')] + extra_headers)
	return [bytes8(doc)] + [bytes8(d) for d in extra_docs]

def ok_text(text, SR, extra_text=[], extra_headers=[]):
	SR('200 OK', [('Content-Type', 'text/plain')] + extra_headers)
	return [bytes8(text)] + [bytes8(t) for t in extra_text]

def ok_urlencoded(content, SR, extra_content=[], extra_headers=[]):
	SR('200 OK', [('Content-Type', 'application/x-www-form-urlencoded')] + extra_headers)
	return [bytes8(content)] + [bytes8(c) for c in extra_content]

def unauth_urlencoded(content, SR):
	SR('401 Unauthorized', [('Content-Type', \
		'application/x-www-form-urlencoded')])
	return [bytes8(content)]

def notfound_urlencoded(content, SR):
	SR('404 Not Found', [('Content-Type', \
		'application/x-www-form-urlencoded')])
	return [bytes8(content)]
