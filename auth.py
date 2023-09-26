import sys, datetime, bcrypt, sqlite3,\
        hashlib, random, html, urllib
import orbit as orb
from orbit import bytes8
import sql, orbgen
from config import CONFIG_SESSION_DAYS, CONFIG_SESSION_MINS

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
            datetime.timedelta(minutes=CONFIG_SESSION_MINS, days=CONFIG_SESSION_DAYS)).timestamp()

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

def get_session_by_username(session_username):
    if session := sql.sessions_get_by_username(session_username):
        return session

def get_session_by_token(session_token):
    if session := sql.sessions_get_by_token(session_token):
        return session

# NOTE: Usage of any password in plaintext outside of this function is a bug
def login(username, password):
    if pwdhash := sql.users_get_pwdhash_by_username(username) and \
            bcrypt.checkpw(bytes8(password), bytes8(pwdhash)):
                return new_session_by_username(username)
