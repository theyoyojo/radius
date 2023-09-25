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

SUBMISSIONS_GET_STUDENT_ASSIGNMENT="""
SELECT (submission_id, student_id, assignment_id,
    submission_name, submission_grade, submission_comments)
FROM submissions
WHERE student_id = "{}"
AND assignment_id = "{}";
""".strip()

ASSIGNMENTS_GET_ALL="""
SELECT *
FROM assignments;
""".strip()

STUDENTS_GET_ID_STUDENT="""
SELECT student_id
FROM students
WHERE username = "{}";
""".strip()

STUDENTS_INSERT_NEW="""
INSERT INTO students (student_id, username)
VALUES ("{}", "{}");
""".strip()

def grades_db_exec(cmd, commit=False):
    print(f"RUN SQL '{cmd}'")
    result = do_sqlite3_comm(cmd, fetch=True, commit=commit)

    return result

def session_enum():
	session_enum.cnt += 1
	return session_enum.cnt
session_enum.cnt = 0

# data = (token,..)
SESSION_GET_TOKEN=session_enum()
SESSION_GET_TOKEN_COMM="""
SELECT token, user, expiry
FROM sessions
WHERE token = "{}";
""".strip()

# data = (...,user,...)
SESSION_GET_USER=session_enum()
SESSION_GET_USER_COMM="""
SELECT token, user, expiry
FROM sessions
WHERE user= "{}";
""".strip()

# data = (token, user, expiry)
SESSION_NEW=session_enum()
SESSION_NEW_COMM="""
INSERT INTO sessions (token, user, expiry)
VALUES ("{}", "{}", "{}");
""".strip()

# data = (token,..)
SESSION_DROP_TOKEN=session_enum()
SESSION_DROP_TOKEN_COMM = """
DELETE FROM sessions
WHERE token = "{}";
""".strip()

# data = (...,user,...)
SESSION_DROP_USER=session_enum()
SESSION_DROP_USER_COMM = """
DELETE FROM sessions
WHERE user = "{}";
""".strip()

def _do_sessions_comm(comm, commit=False, fetch=False):
	return do_sqlite3_comm(SESSIONS_DB, comm, commit=commit, fetch=fetch)

def do_sessions_comm(comm, US=None):
	if	 comm == SESSION_NEW:
		return _do_sessions_comm(SESSION_NEW_COMM % US, commit=True)
	elif comm == SESSION_GET_TOKEN:
		return _do_sessions_comm(SESSION_GET_TOKEN_COMM % (US_token(US)), fetch=True)
	elif comm == SESSION_GET_USER:
		return _do_sessions_comm(SESSION_GET_USER_COMM % (US_user(US)), fetch=True)
	elif comm == SESSION_DROP_TOKEN:
		return _do_sessions_comm(SESSION_DROP_TOKEN_COMM % (US_token(US)), commit=True)
	elif comm == SESSION_DROP_USER:
		return _do_sessions_comm(SESSION_DROP_USER_COMM % (US_user(US)), commit=True)
	else:
		DEBUG("unknown sessions comm type")
		return None	

USERS_GET_PWDHASH="""
SELECT pwdhash
FROM users
WHERE username = "{}"
""".strip()
