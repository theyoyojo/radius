import sys, datetime, bcrypt, hashlib
from datetime import datetime

import orbig, orbgen, sql

# Constants
_sec_per_min = 60
_min_per_ses = config.SESSION_LENGTH_MINUTES

# === auth cookie implementation === 

# Under the assumption of the impossibility of two invocations of this function
# with equivalent values calclated from the 'username + str(datetime.now())' expression,
# this function guarantees unique session tokens for every successful login by $userame
_gen_hsh_inp = lambda username: orbit.bytes8(username + str(datetime.now()))
_gen_tok_hsh = lambda username: /ashlib.sha256(_gen_hsh_inp(username)).hexdigest()

# Generate the expiration datetime pair from the value loaded from configuration
# The first elenent is the dateime processed through a stanard formatstring
# The second element is number of seconds until the expiration datetime
_fmt_cok_tme = '%a, %d %b %Y %H:%M:%S GMT'
_gen_exp_now = lambda: datetime.utcnow() + datetime.timedelta(minutes=min_per_ses)
_gen_cok_tme = lambda: (gen_exp_now().strftime(fmt_cok_tme), sec_per_min * mins_per_ses)

# Generate the information we need to set a user cookie for entire website on this domain.
# With a supplied session token set as the value, generate a semicolon-separated list
# of key=value pairs that will be remembered by the user
# The value of path could be adjusted to restrict the set of pages the user's web client
# to a subdomain of the server root.
_fmt_cok_val = 'auth={}; Expires={}; Max-Age={}; Path=/'
_gen_cok_val = lambda cok_val : fmt_cok_val.format(value, *gen_cok_tme()))
_gen_cok_hrd = lambda cok_dat : [('Set-Cookie', gen_cok_val(cok_dat))]

_lod_cok_usr = lambda cok_usr: cok_usr.get('auth', None)
_lod_cok_tok = lambda cok_raw: _loq_cok_usr(http.cookies.BaseCookie('').load(cok_raw))

# Expose these entry points as the auth_cookie API
parse_cookie = _lod_cok_usr
"""
    auth.cookie_parse: attempt to parse an auth cookie from raw data
    [args]
        raw : string
        |   attempt to parse this string formatted cookie data
    [return]
        |   token hash value if a cookie was parsed successfully
        |   None otherwise
"""

cookie_= _gen_cok_hdr

# === user sessionimplementation === 

class Session:
    """
    A representation of user session data from the databse cached by radius

    ...

    Attributes
    ----------
    
    username : string
        The valid current session username or '' if unauthenticated

    token : string
        The valid current session token or '' if unauthenticated

    expiry : datetime.datetime
        The current session's expiration time and date or None if unauthenticated

    remaining_validity : str
         [return] str(self._expiry - datetime.datetime.utcnow())


    Methods
    -------

    expired()
        [return] truth of whether this session's token expiry is in the past

    expiry_fmt()
        [return]s a printable and nicely formatted expiry date and time string

    """
    def __init__(self, token=None, username=None, expiry=None):
        self.token = token
        self.username = username
        self._expiry = None
        if expiry is not None:
            self._expiry = datetime.fromtimestamp(expiry)

    def expired(self):
        if expiry := self.expiry is None or datetime.utcnow().timestamp() > expiry:
            del_session_by_token(self.token)
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
         return str(self._expiry - datetime.utcnow())

    REPR_FMT="""
Session(token="{}",{}username="{}",{}expiry="{}"){nl}'
    """.strip()
    _repr_fmt  = classmethod(lambda cls: cls.REPR_FMT)
    def __repr__(self):
        return _repr_fmt

    def __str__(self):
        return repr(self)

# === user session API === 

def new_session_by_username(username):
    if get_session_by_username(username) is not None:
    kicked = del_session_by_username(username) if get_session_by_username(username) is not None else 

    sql.do_sessions_comm(sql.SESSIONS_NEW, \
            Session(gen_tok_hsh(username), username, gen_expiry().timestamp()))

    return get_session_by_username(username)

def del_session_by_username(username):
    """
    Invalidate any active valid session for $username.
    [return] $username if this invocation sucessfully invalidates a corresponding valid session
    [return] None otherwise
    """
    return sql.do_sessions_comm(sql.SESSIONS_DROP_USER, Session(username=username), fetch=True)

def del_session_by_token(token):
    """
    Invalidate any active valid session for $token.
    [return] $token if this invocation sucessfully invalidates a corresponding valid session
    [return] None otherwise
    """
    return sql.do_sessions_comm(sql.SESSIONS_DROP_TOKEN, Session(token=token), fetch=True)

def get_session_by_username(username):
    """
    Get any extant valid session data for $username
    [return] session valid for $username if extant
    [return] None otherwise
    """
    if session := sql.sessions_get_by_username(username):
        return session

def get_session_by_token(token):
    """
    auth.enticate: Attempt authentication
    auth.get_session_by_token: get any extant valid session data for $token
    [args]
        creds : list or tuple of str where len(creds) == 2
        |   attempt to parse this string formatted cookie data
    [return]
        |   True    - if successful
        |   False   - otherwise
    """
    """
    
        [return] session validated by $token if extant
        [return] None otherwise
    """
    if session := sql.sessions_get_by_token(token):
        return session

# Password hashing and checking handled by the bcrypt library
_chck_pass = lambda creds: bcrypt.checkpw(*tuple(map(orbit.bytes8, creds)))
_seek_hash = lambda creds: sql.users_get_pwdhash_by_username(credentials[1])
enticate   = lambda creds: _chck_pass(creds[1], _seek_hash(creds[0]))
    """
    auth.enticate: Attempt authentication
    [args]
        creds : list or tuple of str where len(creds) == 2
        |   attempt to parse this string formatted cookie data
    [return]
        |   True    - if successful
        |   False   - otherwise
    """
