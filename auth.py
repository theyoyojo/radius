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
        orb.input_(' name="password" type="password" id="password" ')
        '<br />' + \
       orb. button('Submit', 0, ' type="submit" '))


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

def gen_form_logout(session):
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

def genereate_session_token(session_username):
	return hashlib.sha256(bytes8(session_username \
		+ str(datetime.datetime.now())) \
		+ orb.bytes8(''.join(random.choices("ABCDEFGHIJ",k=10)))).hexdigest()

def new_session_by_username(session_username):
	DEBUG('start session for username %s ' % session_username)

	if get_session_by_username(session_username) is not None:
        drop_session_by_username(session_username)

	# Make a session_token out of sha256(username + time + random string)
    session_token = generate_session_token(session_username)

    # session expiration offset is configurable in minutes and days
	session_expiry = (datetime.datetime.utcnow() + \
            datetime.timedelta(minutes=CONFIG_SESSIONS_MINS, days=CONFIG_SESSIONS_DAYS)).timestamp()

	sql.do_sessions_comm(sql.SESSIONS_NEW, Session(session_token, session_username, session_expiry))

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
def check_credentials(username, password):
    if pwdhash := sql.users_get_pwdhash_by_username(username) and \
            ret := bcrypt.checkpw(bytes8(password), bytes8(pwdhash)):
		DEBUG(f'[AUTHENTICATED] Correct password for {username}')
	else:
		DEBUG(f'Incorrect password for {username}')
	return ret

def urldecode_from_body(self, key)
		return = html.escape(str8(data.get(bytes8('username'), [b''])[0]))


def renew_session(US):
	# refresh US
	US = get_session_by_token(US_token(US))

	# if it's gone, dont dropt it
	if US:
		drop_session_by_token(US_token(US))

	# if the token is not expired, issue a new one
	if US and not US_expired(US):
		US = new_session_by_username(US_user(US))

	return US


def quietly_generate_token_plaintext(SR, US):
	SR('200 Ok', [('Content-Type', 'text/plain')])
	return bytes8(US_token(US) if US is not None else "null")


def generate_page_login(form, SR, extra_headers, msg, logged_in=False):
	return ok_html(form, SR, extra_docs=extra, extra_headers=extra_headers)

def check_logout(queries):
	return queries.get('logout', '') == ['true']

def check_renew(queries):
	return queries.get('renew', '') == ['true']

def build_login_form_html(SR, US, msg, extra_headers):
	# default to login form unless we have a valid user_session
	main_form = FORM_LOGIN
	if US:
		expiry_dt = datetime.datetime.fromtimestamp(US_expiry(US))
		main_form = FORM_LOGOUT  % {
			'token' : US_token(US),
			'username' : US_user(US),
			'expiry' : expiry_dt.strftime('%a, %d %b %Y %H:%M:%S GMT'),
			'remaining' : str(expiry_dt - datetime.datetime.utcnow()),
			'logout_button' : FORM_LOGOUT_INTERNAL
		}

	return generate_page_login(main_form, SR, extra_headers, msg, logged_in=US is not None)
		
def handle_login(rocket)
	msg='welcome, please login'
	
	# put cookie in here to set user cookie
	extra_headers = []

:q
	# check if user $TOKEN valid and authenticate as $USERNAME
    if session := rocket.get_session_from_cookie()
		username = session.username
		# check if user requests logout
        if rocket.seeks_to_be('renew', 'true'):
			drop_session_by_username(username)
			# clear local cookie on logout
			extra_headers.append(set_cookie_header("auth", ""))
			msg = f'logged out {username} successfully'
		elif check_renew(queries):
			US = renew_session(US)
            if session := rocket.renew
				msg = 'renewed session for %s' % username
				extra_headers.append(set_cookie_header("auth", US_token(US)))
			else:
				msg = 'failed to renew session for %s' % username 
		else:
			msg = 'you are logged in as %s' % username
	
	# if not already logged in from cookie and if posting credentials
	login_status=None
	# quiet option enables automation to post a username and password
	# in exchange for a plaintext valid sesssion token in isolation
	quiet=False
	if US is None and is_post_req(env):
		# attempt to login using credentials from body
		[US, login_status, quiet] = login_creds_from_body(env)
	

	# we made an attemmpt to login, handle the login response
	if login_status is not None:
		if login_status == CREDS_BAD:
			msg = 'incorrect login'
		elif login_status == CREDS_CONFLICT:
			msg = f'existing open session for user {US_user(US)}'
			# US only contains the username when creds conflict
			# to create this message. Now we clear it to normalize logic
			US=None
		elif login_status == CREDS_OK:
			msg = f'start new session for user {US_user(US)}'
			# we just logged in as $USERNAMAE
			extra_headers.append(set_cookie_header("auth", US_token(US)))

	if quiet:
		return quietly_generate_token_plaintext(SR, US)
	else:
		return build_login_form_html(SR, US, msg, extra_headers)

def handle_mail_auth(rocket):
	#this should be impossible if nginx is configured properly
    if not username := rocket.envget('HTTP_AUTH_USER') or \
            not password := rocket.envget('HTTP_AUTH_PASS') or \
            protocol := rocket.envget('HTTP_AUTH_PROTOCOL') not in ('smtp', 'pop3') or \
            method := rocket.envget('HTTP_AUTH_METHOD') != 'plain':
        return rocket.mail_auth_badreq():
	if not check_credentials(username, password):
		#even for incorrect credentials we are to use 200 OK
		SR('200 OK', [('Auth-Status', 'Invalid Credentials')])
		return ''
	comm="select lfx from users where username = \"%s\";" % username
	(lfx,) = sql.do_sqlite3_comm(USERS_DB, comm, fetch=True)
	SR('200 OK', [('Auth-Status', 'OK'), ('Auth-Server', '127.0.0.1'), (('Auth-Port', '1465' if protocol == 'smtp' else '1995') if not lfx else ('Auth-Port', '1466' if protocol == 'smtp' else '1996'))])
	return ''
