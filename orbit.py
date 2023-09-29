#!/bin/env python3

import requests, os, sys, http, urllib
from config import SESSION_LENGTH_MINUTES, LOGO_PATH, STYLE_PATH
from urllib.parse import parse_qs

# Application constants
# TODO: move to config?

APPLICATION = 'radius'
VERSION = '0.1'
SOURCE = 'https://github.com/underground-software/radius'
ORBIT_PREFIX = os.environ.get('ORBIT_PREFIX')
HOSTNAME = os.environ.get('SRVNAME')
DATA_ROOT = f'{ORBIT_PREFIX}{HOSTNAME}'

class Rocket:
    """
    orbit.Rocket: Orbit user request context

    ...

    Attributes
    ----------

    path_info : str
        Absolute path requested by user

    queries : dict
        Dictionary of parsed URL queries (passsed by '?key1=value1&key2=value2' suffix)

    session : auth.Session
        The current valid session token if it exists or None

    username : string
        The valid current session username or '' if unauthenticated

    token : string
        The valid current session token or '' if unauthenticated

    expiry : datetime.datetime
        The current session's expiration time and date or None if unauthenticated

    remaining_validity : dattime.timedelta
         Time remaining remaining until session expiry
         return str(self._expiry - datetime.datetime.utcnow())

    Methods
    -------

    expiry_fmt()
        returns a printable and nicely formatted expiry date and time string

    env_get(self, key):
        try to get

    def alert(self, msg):
        self._alerts += [f'<hr /><i>{msg}</i><hr />']

    """

    def __init__(self, environ, start_res):
        self._environ   = environ
        self._start_res = start_res
        self._path_info = None
        self._queires   = None
        self._session   = None
        self._from_user = None
        self._alerts    = None
        self._msg       = "(silence)"
        self._headers   = []
        self._format    = lambda x: x
        # Eventually, toggle CGI or WSGI
        self._raw_body  = lambda self: parse_qs(self.env_get('wsgi.input').read())


    def __repr__(self, tab='', nl='', end=''):
        return ( f'ROCK ({nl}'
                 f'COOK:{tab}{self._user_token}{nl}'
                 f'SESH:{tab}{str(self._session)}{nl}'
                 f'METH:{tab}{self._method_str()}{nl}'
                 f'HEAD:{tab}{self.headers}{nl}'
                 f'MESG:{tab}{self._msg}{nl}'
                 f'QURY:{tab}{self._queries}{nl}'
                 f'PATH:{tab}{self._path_info}{nl}'
                 f'){end}' )

    def __str__(self):
        return repr(self, tab='\t', nl='\n\t', end='\n')

    def env_get(self, key):
        return self._environment.get(key, '')

    def alert(self, msg):
        self._alerts += [f'<hr /><i>{msg}</i><hr />']

    def msg(self, msg):
        self._msg = msg

    def destination(self):
        return ['UML', 'LFX'][sql.users_get_lfx_by_username(username) is not None]

    @property
    def method(self):
        return ['GET', 'POST'][int(self.environ.get('CONTENT_LENGTH', 0)) > 0]

    @property
    def queries(self):
        if self._queries is None:
            self._queries = self.env_get("QUERY_STRING")
        return self._queries

    def _token_from_cookie(self):
        if (auth := auth.load_cookie(self.env_get)):
            self._user_token = auth.value
            return self._user_token

    def _token_from_query(self):
        if token := self.queries.get('token'):
            self._user_token = token
            return self._user_token

    def _token_from_user(self):
        if self._user_token is not None:
            return self._user_token
        # token passed as query overrides local cookie
        if self._token_from_query() or self._token_from_cookie():
            return self._user_token

    @property
    def session(self):
        if self._session is None:
            if self._token_from_user():
                self._session = auth.get_by_token(self._user_token)
            else:
                return None
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

    # Attempt login using urelencoded credentials from request boy
    # or directly attempt login
    def launch(self, username='', password=''):
        if self.is_post_req():
            urldecode = lambda key: html.escape(str8(self.queries.get(bytes8(key), [b''])[0]))
            username = urldecode('username')
            password = urldecode('password')
        self._session = auth.login(username, password)
        if self.token:
            self.headers += auth.hdfor_cookie(self.token)
        return self.session is not None

    # Renew current sesssion and set user auth cookie accordingly
    def refuel(self):
        auth.del_by_username(self.username)
        self._session = auth.new_sesion_by_username(self.username)
        if self.session:
            self.extra_headers += auth.gen_cookie(self.token)
        return self.session

    # Logout of current session and clear user auth cookie
    def retire(self):
        self.extra_headers += auth.gen_cookie('auth', '')
        return auth.del_by_username(self.username)

    # Set appropriate headers
    def parse_content_type(self, content_type):
        match content_type.split('/'):
            case ['text', subtype]:
                self.headers += [('Content-Type', f'text/{subtype}')]
                if subtype == 'html':
                    self.format = self.format_html
            case ['auth', 'badreq']:
                self.headers += [('Auth-Status', 'Invalid Request')]
            case ['auth', 'badcreds']:
                self.headers += [('Auth-Status', 'Invalid Credentials')]
            case ['auth', auth_port]:
                self.headers += [('Auth-Status', 'OK'),
                                 ('Auth-Port',    auth_port),
                                 ('Auth-server', '127.0.0.1')]
            case _:
                return False
        return True

    def format_html(self, doc):
        # generate a reproduction of the original header without too much abstraction for initial version

        # general constant 
        TITLE   = 'Kernel Development Learning Pipeline'
        HR      = '<hr />'
        BR      = '<br />'
        APP_VERSION_SRC     = f'{APPLICATION} {VERSION} {SOURCE}'
        LINK_STYLE_CSS      = '<link rel="stylesheet" type="text/css" href="/style.css />'
        META_CHARSET_UTF8   = '<meta charset="UTF-8">'

        # Prepare logo
        logo_div_doc  = ''
        logo_div_doc += orbgen.img('/kdlp_logo.png', '[KDLP] logo', 'kdlp_logo')
        logo_div_doc += orbgen.h1(TITLE, "title")
        logo_div_gen  = lambda: orbgen.div(' class="logo" ', logo_div_doc)

        # Prepare nav
        # FIXME: consider config
        nav_kvs = [
            (       '/index.md', 'Home'     ),
            ('/course/index.md', 'Course'   ),
            (          '/login', 'Login'    ),
            (       '/register', 'Register' ),
            (      '/dashboard', 'Dashboard'),
            (         '/who.md', 'Who'      ),
            (        '/info.md', 'Info'     ),
            (           '/cgit', 'Git'      )]
        nav_btn_gen =    lambda: ''.join([orbgen.nav_button(pair[0], pair[1]) for pair in nav_kvs])
        nav_div_gen =    lambda: f'{HR}\n{orbgen.div("nav", nav_btn_gen())}\n{HR}\n'

        # Prepare footer
        msg_doc  = ''
        msg_doc += [('application', APPLICATION)]
        msg_doc += [(    'version', VERSION)]
        msg_doc += [(     'source', SOURCE)]
        msg_doc += [(        'msg', self._msg)]
        msg_fmt = lambda kv: orbgen.code(attrs='', c='{} = {}').format(*kv)
        msg_blk = lambda brdr, kvs: brdr + ''.join([msg_fmt(kv) for kv in kvs])

        # Concatenate all components to complete this format operation
        output = ''
        output += LINK_STYLE_CSS
        output += META_CHARSET_UTF8
        output += logo_div_gen()
        output += nav_div_gen()
        output += doc
        output += msg_blk(msg_doc)

        return output

    def respond(self, *content_desc):
        # Given total correctness of the server
        # all user requests end up here
        match content_desc:
            case (code, content_type, content) if self.parse_content_type(content_type):
                document = self.format(content)
            case _:
                self.parse_content_type('text/plain')
                code = http.HTTPStatus.INTERNAL_SERVER_ERROR
                document = 'ERROR: BAD RADIUS CONTENT DESCRIPTION'
        self._start_response(f'{code.value} {code.phrase}', self.headers)
        return [bytes8(document)]
