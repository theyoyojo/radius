import sys, datetime, bcrypt, sqlite3, hashlib, random, html, urllib

from config import SESSIONS_DAYS, SESSIONS_MINS

from orbit import DEBUG, bytes8, str8
import orbit as orb
import sql

def gen_form_login():
    return orb.form(' id="login" method="post" action="/login" ',
        orb.label(' for="username" ', 'Username: <br />') + \
        orb.input_(' name="username" type="text" id="username" ') + \
        '<br />' + \
        orb.label(' for="username" ', 'Username: <br />') + \
        orb.input_(' name="password" type="password" id="password" ') + \
        '<br />' + \
        orb.button('Submit', 0, ' type="submit" '))


def gen_cookie_info_table(session):
    return orb.table([
        ('Cookie Key', 'Value'),
        ('Token', session.token),
        ('User', session.username),
        ('Expiry', session.expiry_fmt),
        ('Remaining Validity', session.remaining_validity)])

def gen_logout_buttons():
    return form(' id="logout" method="get" action="/login" ', \
        orb.input_(' type="hidden" name="logout" value="true" ') + \
        orb.button('Logout', 0, ' type="submit" class="logout" ')) + \
        orb.form(' id="rewnew" method="get" action="/login" ',
        orb.input_(' id="renew" method="get" action="/" ') + \
        orb.button('Renew', 0, ' type="submit" class="renew" '))

def gen_form_authorized(session):
    return orb.div(orb.div(gen_cookie_info_table(session), ' class="logout_left" ') + \
        orb.div(orb.h5("Welcome!") + orb.ul([orb.a('Dashboard', '/dashboard')]) + \
        orb.div(gen_logout_buttons() ,' class="logout_buttons" '), ' class="logout_info" ')

# Source: https://stackoverflow.com/questions/14107260/set-a-cookie-and-retrieve-it-with-python-and-wsgi
def set_cookie_header(name, value, days=SESSIONS_DAYS, minutes=SESSIONS_MINS):
	dt = datetime.datetime.now() + datetime.timedelta(days=days,minutes=minutes)
	fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
	secs = 60 * minutes + 86400 * days
	return ('Set-Cookie', '{}={}; Expires={}; Max-Age={}; Path=/'.format(name, value, fdt, secs))

class Session:
    def __init__(self, token=None, username=None, expiry=None):
        self.token = token
        self.username = username
        self._expiry = None
        if expiry is not None:
            self._expiry = datetime.datetime.fromtimestamp(expiry)

    def expired(self):
          if expiry := self.expiry is None or datetime.datetime.utcnow().timestamp() > expiry:
            drop_session_by_token(self.token)
            return True
        else:
            return False

    def expiry_fmt(self):
        return self._expiry.strftime('%a, %d %b %Y %H:%M:%S GMT')

    @property
    def expiry(self):
        return self._expiry.timestamp()

    @property
    def remaining_validity(self):
         return str(self._expiry - datetime.datetime.utcnow())

    def __repr__(self):
        return f'Session(token="{self.token}", username="{self.username}", expiry="{self.expiry}")'

    def __str__(self):
        return repr(self)

def gen_session_token(session_username):
	return hashlib.sha256(bytes8(session_username \
		+ str(datetime.datetime.now())) \
		+ orb.bytes8(''.join(random.choices("ABCDEFGHIJ",k=10)))).hexdigest()

def calc_new_session_expiry():
    # session expiration offset is configurable in minutes and days
	return (datetime.datetime.utcnow() + \
            datetime.timedelta(minutes=CONFIG_SESSIONS_MINS, days=CONFIG_SESSIONS_DAYS)).timestamp()

def new_session_by_username(session_username):
	if get_session_by_username(session_username) is not None:
        drop_session_by_username(session_username)

	sql.do_sessions_comm(sql.SESSIONS_NEW, \
            Session(gen_session_token(session_username), session_username, calc_new_session_expiry))

	return get_session_by_username(session_username)

def drop_session_by_username(session_username):
    session_before = get_session_by_username(session_username)
	sql.do_sessions_comm(sql.SESSIONS_DROP_USER, Session(username=session_username))
    session_after = get_session_by_username(session_username)
    if session_before is not None and session_after is None:
        return session_usernae

def drop_session_by_token(session_token):
    session_before = get_session_by_token(session_token)
	sql.do_sessions_comm(sql.SESSIONS_DROP_TOKEN, Session(token=session_token))
    session_after = get_session_by_token(session_token)
    if session_before is not None and session_after is None:
        return session_before.username

def get_session_by_func(session_key, session_partial, sql_comm, get_session_by, drop_session_by):
    if session := do_sessions_(sql_comm, session_partial) and not session.expired():
        return session

def get_session_by_username(session_username)
    if session := g
    (sql_comm, session_partial) and not session.expired():
        
    if session := get_session_by_username(session_username, Session(username=session_usename), \
            sql.SESSIONS_GET_USER, get_session_by_username, drop_session_by_username)

# return none if token is expired and also purge old entry
def get_session_by_token(session_token):
    return get_session_by_func(session_token, Session(token=session_token), \
            sql.SESSIONS_GET_TOKEN, get_session_by_token, drop_session_by_token)

# NOTE: Usage of any password in plaintext outside of this function is a bug
def login(username, password):
    if pwdhash := sql.users_get_pwdhash_by_username(username) and \
            bcrypt.checkpw(bytes8(password), bytes8(pwdhash)):
            return new_session_by_username(username)
