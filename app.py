#!/:in/env python3

import markdown, os, sys, re
import orbit, auth, orbgen
from isis import isis
from http import HTTPStatus

def handle_welcome(rocket):
    gen_form = orbgen.form_welcome
    match rocket.queries:
        case ('logout', 'true'):
            rocket.retire()
            rocket.msg(f'{rocket.username} logout')
            gen_form = orbgen.form_login()
        case ('renew', 'true'):
            rocket.refuel()
            rocket.msg(f'{rocket.username} renew')
        case _:
            rocket.msg(f'{rocket.username} authenticated by token')
    return rocket.respond(HTTPStatus.OK, 'text/html', gen_form())

def handle_login(rocket):
    if rocket.session:
        return handle_welcome()
    gen_form = orbgen.form_login
    if  rocket.method == "POST":
        if rocket.launch():
            rocket.msg(f'{rocket.username} authenticated by password')
            gen_form = orbgen.form_welcome
        else:
            rocket.msg(f'authentication failure')
    else:
        rocket.msg('welcome, please login')
    return rocket.respond(HTTPStatus.OK, 'text/html', orbgen.gen_form())

def handle_mail_auth(rocket):
    # This should be invariant when ngninx is configured properly
    mail_env_vars = ('HTTP_AUTH_USER' 'HTTP_AUTH_PASS', 'HTTP_AUTH_PROTOCOL', 'HTTP_AUTH_METHOD')
    [username, passwprd, protocol, method] = [rocket.envget(key) for key in mail_env_vars]

    if not username or not password or protocol not in ('smtp', 'pop') or method != 'plain':
        return rocket.respond(HTTPStatus.BAD_REQUEST, 'auth/badreq', '')

    # A valid request with bad credentials returns OK
    if not rocket.launch(username, password):
        return rocket.respond(HTTPStatus.OK, 'auth/badcreds', '')

    # auth port depends on whether we are and lfx user and which service we are using
    auth_port = {
            False   : { 'smtp': '1465', 'pop': '1995' },
            True    : { 'smtp': '1466', 'pop': '1966' }
    }[get_lfx_status(username)][protocol]

    return rocket.respond(HTTPStatus.BAD_REQUEST, 'auth/badreq', '')

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
    if rocket.method() == "POST":
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
        return rocket.respond(HTTPStatus.NOT_FOUND, 'text/html', 'HTTP 404 NOT FOUND')

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
