#!/bin/env python3

import markdown, os, sys, re
import orbit, auth

def handle_check(rocket):
    if token := rocket.seeks('token') and session_found := auth.get_session_by_token(token):
        return rocket.ok_text(session_found.user)
    else:
        return rocket.illegal_text('null')

def handle_logout(rocket):
    if user := rocket.seeks('user'):
        return rocket.ok_text(auth.drop_session_by_username(user))
    else:
        return rocket.illegal_text('null')

def handle_dashboard(rocket):
    return rocket.ok_html(isis(rocket.user))

def handle_md(rocket):
    with open(fname, 'r', newline='') as f:
        return rocket.ok_html(markdown.markdown(f.read(), extensions=['tables', 'fenced_code']))

def try_handle_md(rocket)
    if re.match("^(?!/cgit)(.*\.md)$", rocket.patch_info) and \
            os.access.(orbit.DATA_ROOT + '/md' + path_info, os.R_OK):
        return handle_md(rocket)
	else:
		return rocket.notfound_html()

def application(env, SR):
    rocket = Rocket(env, SR)
    if re.match("^(/login|/check|/logout/|/mail_auth)", rocket.path_info):
        return handle_auth(rocket)
    elif re.match("^/dashboard", rocket.path_info):
		return handle_dashboard(rocket)
    else:
        return try_handle_md(rocket)
