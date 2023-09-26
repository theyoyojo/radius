#!/:in/env python3

import markdown, os, sys, re
import orbit, auth, orbgen
from isis import isis

def handle_authenticated_login(rocket):
        if rocket.seeks_to_find('logout', 'true'):
            rocket.retire()
            rocket.caplog(f'{rocket.username} logout')
            return rocket.ok_html(orbgen.form_login())
        elif rocket.seeks_to_find('renew', 'true'):
            rocket.refuel()
            rocket.caplog(f'{rocket.username} renew session')
        else:
            rocket.caplog(f'{rocket.username} authenticated by token')
        return rocket.ok_html(orbgen.form_authorized())

def handle_authorization_attempt(rocket):
    if rocket.launch():
        rocket.caplog(f'{rocket.username} authenticated by password')
        return rocket.ok_html(orbgen.form_authorized())
    else:
        rocket.caplog(f'authentication failure')
        return rocket.ok_html(orbgen.form_login())

def handle_unauthorized_login(rocket):
    if rocket.is_post_req():
        return handle_authorization_attempt(rocket)
    else:
        rocket.caplog('welcome, please login')
        return rocket.ok_html(orbgen.form_login())

def handle_login(rocket):
    if rocket.session:
        return handle_authenticated_login(rocket)
    else:
        return handle_unauthorized_login(rocket)

def handle_mail_auth(rocket):
    # This should be invariant when ngninx is configured properly
    if username := rocket.envget('HTTP_AUTH_USER') is None:
        return rocket.mail_auth_badreq()
        
    if password := rocket.envget('HTTP_AUTH_PASS') is None:
        return rocket.mail_auth_badreq()

    if protocol := rocket.envget('HTTP_AUTH_PROTOCOL') not in ('smtp', 'pop3'):
        return rocket.mail_auth_badreq()

    if method   := rocket.envget('HTTP_AUTH_METHOD') != 'plain':
        return rocket.mail_auth_badreq()

    if not login(username, password):
        return rocket.mail_auth_ok_invalid()

    # auth port depends on whether we are and lfx user and which service we are using
    auth_port = {
            False   : { 'smtp': '1465', 'pop': '1995' },
            True    : { 'smtp': '1466', 'pop': '1966' }
    }[get_lfx_status(username)][protocol]

    return rocket.mail_auth_ok(auth_port)

def handle_check(rocket):
    if token := rocket.seeks('token'):
        session_found = auth.get_session_by_token(token)
        return rocket.ok_text(session_found.user)
    else:
        return rocket.illegal_text('null')

def handle_logout(rocket):
    if user := rocket.seeks('username'):
        return rocket.ok_text(auth.drop_session_by_username(user))
    else:
        return rocket.illegal_text('null')

def handle_dashboard(rocket):
    return rocket.ok_html(isis(rocket.user))

def handle_register(rocket):
    if rocket.is_post_req():
        # TODO
        pass
        
    return rocket.ok_html(orbgen.form_register())

def handle_md(rocket):
    with open(fname, 'r', newline='') as f:
        return rocket.ok_html(markdown.markdown(f.read(), extensions=['tables', 'fenced_code']))


def try_handle_md(rocket):
    if re.match("^(?!/cgit)(.*\.md)$", rocket.path_info) and \
            os.access(f'{orbit.DATA_ROOT}/md{rocket.path_info}', os.R_OK):
        return handle_md(rocket)
    else:
        return rocket.notfound_html('HTTP 404 Not Found')

def application(env, SR):
    rocket = orbit.Rocket(env, SR)

    if re.match("^(/login|/check|/logout/|/mail_auth)", rocket.path_info):
        return handle_auth(rocket)
    elif re.match("^/dashboard", rocket.path_info):
        return handle_dashboard(rocket)
    elif re.match("^/register", rocket.path_info):
        return handle_register(rocket)
    else:
        return try_handle_md(rocket)
