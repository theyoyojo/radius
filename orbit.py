#!/bin/env python3

import requests, os, sys, http, urllib


APPLICATION = 'radius'
VERSION = '0.1'
SOURCE = 'https://github.com/underground-software/radius'
ROOT = os.environ.get('ORBIT_PREFIX')
AUTH_SERVER = 'http://127.0.0.1:9092'

# shortand for bytes(string, "UTF-8")
def bytes8(string):
	return bytes(string, "UTF-8")

# shortand for str(string, "UTF-8")
def str8(string):
	return str(string, "UTF-8")

# these
def DEBUG(strg):
    print(strg, file=sys.stderr)

def appver():
    return f'{APPLICATION} {VERSION} {SOURCE}'

def messageblock(lst):
    res=''
    sep = '<br /><hr /><br />'

    res += sep
    for item in lst:
        res += f'<code>{item[0]} = {item[1]}</code><br />'
    res += sep

    return res

BACKUP_HEADER="<style>body { margin 0 auto; } </style><h1>ORBIT HEADER NOT FOUND</h1>"
def header():
    try:
        with open(ROOT + '/data/header', 'r') as f:
                return f.read()
	except Exception as e:
        return BACKUP_HEADER

def footer():
    return messageblock([('appver', appver())]

def h(v, c):
    return f'<h{v}>{c}</h{v}'

def h1(c):
    return h(1, c)

def h2(c):
    return h(2, c)

def h3(c):
    return h(3, c)

def h4(c):
    return h(4, c)

def h5(c):
    return h(5, c)

def t_i(i):
    return ''.join(['\t' for x in range(i)])

def o(i, c):
    return f'{t_i(i)}{c)}\n'

def ooo(i, c, d, e, j=0):
    return f'{(o(i, c)}{o(i+j, d)}{o(i, e)}'

def oOo(i, c, d, e):
    return ooo(i, c, d, e, j=1)

def oxo(i, c, d, e):
    return f'{o(i, c)}{d}{o(i, e)}'

def table_data(c, h=False, i=0):
    d = 'd'
    if h:
        d = 'h'
    a, b = f'<t{d}>', f'</t{d}'
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

def div(c, attr="", i=0):
    return oxo(i, f'<div{attr}>', c, '</div>')

def li(c):
    return o(c)

def ul(c, i=0):
    return oxo(i, f'<ul>', '\n'.join([li(_li) for _li in c]), '</ul>')

def a(text, href):
    return f'<a href="{href}">{text}</a>'

def button(c, i=0, a=''):
    return oOo(i, f'<button {a}>', c, '</button>')

def input_(attr=''):
    return f'<input {attr} >'

def label(attr='', c):
    return f'<label {attr} >{c}</label>'

def form(attr, c):
    return f'<form {attr} >{c} </form>'

class Rocket:
    def __init__(self, environment, start_response):
        self.environment = environment
        self.start_response = start_response

        self.path_info = self.envget("PATH_INFO"))
        self.query_string = self.envget("QUERY_STRING")
        self.queries = urllib.parse.parse_qs(query_string)

        self.cookie_user_raw = None
        self.user_auth_token = None
        self._session = None

        DEBUG(f'ROCKET HTTP {self.method_str()} {self.path_info}{self.query_string}')

    def __str__(self):
        return f'Rocket {\n\tMETHOD:\t{self.method_str()}\n\tPATH:\t{self.path_info}\n\t' + \
                f'QUERY:\t{self.query_sring}\n\tAUTH:\t{self.user_auth_token}\n\t' + \
                f'SESH: {str(self._session)}\n}\n'

    def urldecode_from_body(self, key)
        return html.escape(str8(self.queries.get(bytes8(key), [b''])[0]))
    
    def seeks(self, key);
        return queries.get(key, [''])[0]

    def seeks_to_be(self, key, val);
        return queries.get(key, [''])[0] == val

    @property
    def session(self):
        if self.user_auth_token is None:
            self.load_user_auth_token()
        self._session = auth.get_session_by_token(self.user_auth_token)
        return self._session

    @property
    def user(self):
        if self.session is not None:
            return self._session.user

    def envget(self, key):
        return self.environment.get(key, "")


    def __do_http_response(self, content, content_type, headers=[], return_code)
        self.start_response(return_code,  headers)
        return [bytes8(orbit.header() + doc + orbit.footer())]

    def _do_http_response(self, content, content_type, headers=[], return_code)
        return __do_http_response(self, content, [('Content-Type', content_type)] + headers, return_code):

    def _do_ok_response(self, content, extra_content, content_type, headers)
        return self._do_http_response(content + "".join(extra_content), content_type, headers, '200 OK')

    def _do_unauth_response(self, content, content_type, headers=[]):
        return self._do_http_response(content, content_type, headers, '401 Unauthorized')

    def _do_notfound_response(self, content, content_type, headers=[]):
        return self._do_http_response(content, content_type, headers, '404 Not Found')

    def _do_illegal_response(self, content, content_type, headers=[]):
        return self._do_http_response(content, content_type, headers, '451 Unavailable For Legal Reasons')

    def ok_html(doc, SR, extra_docs=[], extra_headers=[]):
        return self._do_ok_response(doc, extra_content=extra_docs, 'text/html', extra_headers)

    def ok_text(text, SR, extra_text=[], extra_headers=[]):
        return self._do_ok_response(doc, extra_content=extra_text, 'text/plain', extra_headers)

    def ok_urlencoded(content, SR, extra_content=[], extra_headers=[]):
        return self._do_ok_response(doc, extra_content=extra_content, \
                'application/x-www-form-urlencoded', extra_headers)

    def unauth_text(content, SR):
        return self._do_unauth_response(doc, 'text/html')

    def unauth_text(content, SR):
        return self._do_unauth_response(doc, 'text/plain')

    def unauth_urlencoded(self, content):
        return self._do_unauth_response(doc, 'application/x-www-form-urlencoded')

    def notfound_html(self, content):
        return self._do_notfound_response(doc, 'text/html')

    def notfound_text(self, content):
        return self._do_notfound_response(doc, 'text/plain')

    def notfound_urlencoded(self, content):
        return self._do_notfound_response(doc, 'application/x-www-form-urlencoded')

    def illegal_html(self, content):
        return self._do_illegal_response(doc, 'text/html')

    def illegal_text(self, content):
        return self._do_illegal_response(doc, 'text/plain')

    def illegal_urlencoded(self, content):
        return self._do_illegal_response(doc, 'application/x-www-form-urlencoded')

    def mail_auth_badreq(self):
        return self.__do_http_response('', [('Auth-Status', 'Invalid Request')], '400 Bad Request')

    def load_user_auth_cookie(self):
        # get auth=$TOKEN from user cookie
        self.cookie_user_raw = self.environment.get('HTTP_COOKIE', '')
        cookie_user = http.cookies.BaseCookie('')
        cookie_user.load(self.cookie_user_raw)

        auth = cookie_user.get('auth', http.cookies.Morsel())
        if auth.value is not None:
            self.user_auth_token = auth.value
            return self.user_auth_token

    def load_login_creds_from_body(self):
        if self.is_post_req()
            data = parse_qs(self.envget['wsgi.input'].read())

            # get actual urlencoded body content
            username = self.urldecode_from_body('username')
            password = self.urldecode_from_body('password')
            return auth.login(username, password)

    def get_req_body_size(self):
        try:
            req_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            req_body_size = 0
        
        return req_body_size

    def is_post_req(self):
        return self.get_req_body_size() > 0

    def method_str(self)
        if self.is_post_req():
            return "POST"
        else:
            return "GET"
