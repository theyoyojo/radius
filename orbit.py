#!/bin/env python3

import requests, os, sys, http, urllib
from config import CONFIG_SESSION_MINS, CONFIG_SESSION_DAYS

# Application constants
# TODO: move to config?

APPLICATION = 'radius'
VERSION = '0.1'
SOURCE = 'https://github.com/underground-software/radius'
ORBIT_PREFIX= os.environ.get('ORBIT_PREFIX')
HOSTNAME = os.environ.get('SRVNAME')
DATA_ROOT = f'{ORBIT_PREFIX}{HOSTNAME}'

# Simply utilitys

def bytes8(string):
	return bytes(string, "UTF-8")

def str8(string):
	return str(string, "UTF-8")

def DEBUG(strg):
    print(strg, file=sys.stderr)

def appver():
    return f'{APPLICATION} {VERSION} {SOURCE}'

def messageblock(lst):
    sep = '<br /><hr /><br />'
    res = sep
    for item in lst:
        res += f'<code>{item[0]} = {item[1]}</code><br />'
    res += sep

    return res

# Source: https://stackoverflow.com/questions/14107260/set-a-cookie-and-retrieve-it-with-python-and-wsgi
def set_cookie_header(name, value, days=CONFIG_SESSION_DAYS, minutes=CONFIG_SESSION_MINS):
	dt = datetime.datetime.now() + datetime.timedelta(days=days,minutes=minutes)
	fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
	secs = 60 * minutes + 86400 * days
	return ('Set-Cookie', '{}={}; Expires={}; Max-Age={}; Path=/'.format(name, value, fdt, secs))

BACKUP_HEADER="<style>body { margin 0 auto; } </style><h1>ORBIT HEADER NOT FOUND</h1>"
class Rocket:
    def __init__(self, environment, start_response):
        self.environment = environment
        self.start_response = start_response

        self.path_info = self.envget("PATH_INFO")
        self.query_string = self.envget("QUERY_STRING")
        self.queries = urllib.parse.parse_qs(self.query_string)

        self.cookie_user_raw = None
        self.user_auth_token = None
        self._session = None
        self.alerts = None
        self.captains_log = None
        self.headers = []
        self.format = lambda x: x

    def __str__(self):
        return ( f'Rocket (\n\t'
                 f'METHOD:\t{self.method_str()}\n\t'
                 f'PATH:\t{self.path_info}\n\t'
                 f'QUERY:\t{self.query_sring}\n\t'
                 f'AUTH:\t{self.user_auth_token}\n\t'
                 f'SESH:\T{str(self._session)}\n'
                 f')\n' )

    def alert(self, msg):
        alerts += [f'<hr /><i>{msg}</i><hr />']

    def caplog(self, msg):
        self.captains_log = msg

    def urldecode_from_body(self, key):
        return html.escape(str8(self.queries.get(bytes8(key), [b''])[0]))

    # usage of Rocket.session idempotently loads the user cookie if it exists
    @property
    def session(self):
        if self.user_auth_token is None:
            self.load_user_auth_token()
            self._session = auth.get_session_by_token(self.user_auth_token)
        return self._session

    @property
    def username(self):
        return self._session.username   if self.session else None

    @property
    def token(self):
        return self._session.token      if self.session else None

    @property
    def expiry(self):
        return self._session.expiry     if self.session else None

    
    def load_user_auth_cookie(self):
        # get auth=$TOKEN from user cookie
        self.cookie_user_raw = self.environment.get('HTTP_COOKIE', '')
        cookie_user = http.cookies.BaseCookie('')
        cookie_user.load(self.cookie_user_raw)

        auth = cookie_user.get('auth', http.cookies.Morsel())
        if auth.value is not None:
            self.user_auth_token = auth.value
            return self.user_auth_token

    # Attempt login using urelencoded credentials from request boy
    # or directly attempt login
    def launch(self, username='', password=''):
        if self.is_post_req():
            data = parse_qs(self.envget['wsgi.input'].read())

            # get actual urlencoded body content
            username = self.urldecode_from_body('username')
            password = self.urldecode_from_body('password')

        self._session = auth.login(username, password)
        if self.session:
            self.extra_headers += set_cookie_header("auth", session.token)

    # Renew current sesssion and set user auth cookie accordingly
    def refuel(self):
        auth.drop_session_by_username(self.username)
        self._session = auth.new_sesion_by_username(self.username)
        if self.session:
            self.extra_headers += set_cookie_header('auth', session.token)
        return self.session

    # Logout of current session and clear user auth cookie
    def retire(self):
        self.extra_headers += set_cookie_header('auth', '')
        return auth.drop_session_by_username(self.username)

    def envget(self, key):
        return self.environment.get(key, '')

    # Set appropriate headers
    def parse_content_type(self, content_type):
        match content_type.split('/'):
            case ['text', subtype]:
                self.headers += [('Content-Type', f'text/{subtype}')]
                if subtype= 'html':
                    self.format = format_html
            case ['auth', 'badreq']:
                self.headers += [('Auth-Status', 'Invalid Request')]
            case ['auth', 'badcreds']:
                self.headers += [('Auth-Status', 'Invalid Credentials')]
            case ['auth', auth_port]:
                self.headers += [('Auth-Status', 'OK'), ('Auth-Port', auth_port),
                        ('Auth-server', '127.0.0.1')]
            case _:
                return False
        return True

    def format_html(self, content):
        output = ''
        try:
            with open(f'{ROOT}/{SRVNAME}/data/header', 'r') as f:
                    output += "".join(self.alerts)
        except Exception as e:
            output += BACKUP_HEADER
        output += content
        output += messageblock(('appver', appver()),
                ('msg', str(self.captains_log))] if self.captains_log is not None else []
        return output

    def respond(self, *content_desciption)
        match content_description:
            case (code, content_type, content) and self.parse_content_type(content_type):
                # This is the __only__ call site of start_respoinse in in this application
                # All user requests eventually end up here 
                document = self.format(content)
            case _:
                self.parse_content_type('text/plain')
                code = http.HTTPStatus.INTERNAL_SERVER_ERROR
                document = 'ERROR: BAD RADIUS CONTENT DESCRIPTION'
            self.start_response(f'{code.value} {code.phrase}', self.headers)
            return document

    def get_lfx_status(self):
        return sql.users_get_lfx_by_username(username) is not None

    def get_req_body_size(self):
        try:
            req_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            req_body_size = 0
        
        return req_body_size

    def is_post_req(self):
        return self.get_req_body_size() > 0

    @ property
    def method(self):
        if self.is_post_req():A
            return "POST"
        else:
            return "GET"
