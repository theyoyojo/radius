#!/usr/bin/env python

import sqlite3

from config import ORBIT_DB

def do_sqlite3_comm(comm, commit=False, fetch=False):
	result=None
	db_con = sqlite3.connect(ORBIT_DB)
	db_cur0 = db_con.cursor()
	
	db_cur1 = db_cur0.execute(comm)

	if fetch:
		result=db_cur1.fetchone()

	if commit:
		db_cur2 = db_cur1.execute("COMMIT;")

	db_con.close()

	return result

SUBMISSIONS_GET_BY_STUDENT_AND_ASSIGNMENT="""
SELECT (submission_id, student_id, assignment_id,
    submission_name, submission_grade, submission_comments)
FROM submissions
WHERE student_id = "{}"
AND assignment_id = "{}";
""".strip()

def submissions_get_by_student_and_assignment(sid, aid):
    do_sqlite3_comm(SUBMISSIONS_GET_STUDENT_ASSIGNMENTS, fetch=True)

ASSIGNMENTS_GET_ALL="""
SELECT *
FROM assignments;
""".strip()

def submissions_get_all():
    do_sqlite3_comm(SUBMISSIONS_GET_ALL, fetch=True)

SESSIONS_GET_BY_TOKEN="""
SELECT token, username, expiry
FROM sessions
WHERE token = "{}";
""".strip()

def sessions_get_by_token(s):
    do_sqlite3_comm(SESSIONS_GET_BY_TOKEN.format(s.token), fetch=True)

SESSIONS_GET_BY_USERNAME="""
SELECT token, username, expiry
FROM sessions
WHERE username = "{}";
""".strip()

def sessions_get_by_username(s):
    do_sqlite3_comm(SESSIONS_GET_BY_USERNAME.format(s.username), fetch=True)

SESSIONS_NEW="""
INSERT INTO sessions (token, username, expiry)
VALUES ("{}", "{}", "{}");
""".strip()

def sessions_new(s):
	return do_sqlite3_comm(SESSIONS_NEW_COMM.format(s.username, s.token, s.expiry), commit=True)

SESSIONS_DROP_BY_TOKEN= """
DELETE FROM sessions
WHERE token = "{}";
""".strip()

def sessions_drop_by_token(s):
	return do_sqlite3_comm(SESSIONS_DROP_BY_TOKEN.format(s.token), commit=True)

SESSIONS_DROP_BY_USERNAME= """
DELETE FROM sessions
WHERE username = "{}";
""".strip()

def sessions_drop_by_username(s):
	return do_sqlite3_comm(SESSIONS_DROP_BY_USER.format(s.name), commit=True)

SESSIONS_GET_ALL="""
SELECT id, username, pwdhash, lfx
FROM users;
""".strip()

def sessions_get_all():
	return do_sqlite3_comm(SESSIONS_GET_ALL, fetch=True)


USERS_GET_PWDHASH_BY_USERNAME="""
SELECT pwdhash
FROM users
WHERE username = "{}"
""".strip()

def users_get_pwdhash_by_username(u):
    return do_sqlite3_comm(USERS_GET_PWDHASH.format(u), fetch=True)

USERS_NEW="""
INSERT INTO users (username, pwdhash, lfx, student_id)
VALUES ("{}", "{}", "{}", "{}");"
""".strip()

def users_new(u, p, l=False, i=0)
    return do_sqlite3_comm(USERS_GET_PWDHASH_COMM.format(u, p, l, i), commit=True)

USERS_GET_LFX_BY_USERNAME="""
SELECT lfx
FROM users
WHERE username = "{}";
""".strip()

def users_get_lfx_by_username(u):
    return do_sqlite3_comm(USERS_GET_LFX_BY_USERNAME.format(u), fetch=True)
