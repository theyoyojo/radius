#!/bin/env python3

import markdown as markdown
import os, sys

import orbit
import auth

HTML_404 = '<h1> 404: PAGE NOT FOUND </h1>'
_500	= '500 Internal Server Error'
_500_MSG=b'500 Internal Server Error\n\nunable to load format pre-reqs'

def read_file(filename, mode='r'):
	output = ''
	with open(filename, mode) as f:
		output += f.read()
	return output

def handle_md(path, SR):
	output=''
	# response to request for directory
	# with index.md page within, it exists
	fname = '%s%s' % (ROOT + '/md', path_info)
	if os.path.isdir(fname):
		fname += '/index.md'

	# return any .md file in MD_ROOT
	try:
		with open(fname, 'r', newline='') as f:
			output += markdown.markdown(f.read(), extensions=['tables', 'fenced_code'])
		status = '200 Ok'
	except Exception as e:
		output += HTML_404
		status = '404 Not Found'

	output += orbit.footer()

	SR(status, [('Content-Type', 'text/html')])
	return [bytes(output, "UTF-8")]

def application(env, SR):
    output += orbit.header()
	try:
            with open(ROOT + '/data/header', 'r') as f:
                    output += f.read()
	except Exception as e:
		SR(_500, [('Content-Type', 'text/plain')])
		return _500_MSG

	path_info = env.get("PATH_INFO", "")
	query_string = env.get("QUERY_STRING", "")
	queries = parse_qs(query_string)

	if len(sys.argv) > 1 and sys.argv[1] == 'test':
            USERS_DB = 'users.test.db'
            SESSIONS_DB = 'sessions.test.db'

	DEBUG("HTTP  path_info=\"%s\", queries=\"%s\"" \
		% (str(path_info), str(queries)))
    
    # cgit exception should be handled by nginx
    if len(path_info) >= 3 and path_info[len(path_info)-3:] == ".md":
        if os.path.isfile(ROOT + '/md' + path_info):
            return handle_md(path)

	if path_info == "/login":
		return auth.handle_login(queries, SR, env)
	elif path_info == "/check":
		return auth.handle_check(queries, SR)
	elif path_info == "/logout":
		return auth.handle_logout(queries, SR)
	elif path_info == "/mail_auth":
		return auth.handle_mail_auth(SR, env)
	else:
		return orbit. 
