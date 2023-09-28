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
    return do_sqlite3_comm(SUBMISSIONS_GET_STUDENT_ASSIGNMENTS, fetch=True)

SUBMISSIONS_GET_ALL="""
SELECT *
FROM submissions;
""".strip()

def submissions_get_all():
    return do_sqlite3_comm(SUBMISSIONS_GET_ALL, fetch=True)

SESSIONS_GET_BY_TOKEN="""
SELECT token, username, expiry
FROM sessions
WHERE token = "{}";
""".strip()

def sessions_get_by_token(s):
    return do_sqlite3_comm(SESSIONS_GET_BY_TOKEN.format(s.token), fetch=True)

SESSIONS_GET_BY_USERNAME="""
SELECT token, username, expiry
FROM sessions
WHERE username = "{}";
""".strip()

def sessions_get_by_username(s):
    return do_sqlite3_comm(SESSIONS_GET_BY_USERNAME.format(s.username), fetch=True)

SESSIONS_NEW="""
INSERT INTO sessions (token, username, expiry)
VALUES ("{}", "{}", "{}");
""".strip()

def sessions_new(s):
    return do_sqlite3_comm(SESSIONS_NEW_COMM.format(s.username, s.token, s.expiry), commit=True)

SESSIONS_DROP_BY_TOKEN= """
DELETE FROM sessions
WHERE token = "{}"
RETURNING username;
""".strip()

def sessions_delete_by_token(s):
    return do_sqlite3_comm(SESSIONS_DROP_BY_TOKEN.format(s.token), commit=True)

SESSIONS_DROP_BY_USERNAME= """
DELETE FROM sessions
WHERE username = "{}"
RETURNING username;
""".strip()

def sessions_delete_by_username(s):
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

def users_new(u, p, l=False, i=0):
    return do_sqlite3_comm(USERS_GET_PWDHASH_COMM.format(u, p, l, i), commit=True)

USERS_GET_ALL="""
SELECT id, username, pwdhash, lfx
FROM users;
""".strip()

def sessions_get_all():
    return do_sqlite3_comm(USERS_GET_ALL, fetch=True)

USERS_GET_LFX_BY_USERNAME="""
SELECT lfx
FROM users
WHERE username = "{}";
""".strip()

def users_get_lfx_by_username(u):
    return do_sqlite3_comm(USERS_GET_LFX_BY_USERNAME.format(u), fetch=True)

SUBMISSIONS_INSERT="""
INSERT INTO submissions (sub_id, username, timestamp, _from, _to, email_ids, subjects)
VALUES ("{}","{}","{}","{}","{}","{}","{}");
""".strip()

def submissions_insert(sub_id, username, timestamp, from_, to_, email_ids, subjects):
    return do_sqlite3_comm(SUBMISSIONS_INSERT.format(sub_id, user, time,
        from_, to_, "\n".join(email_ids), "\n".join(subjects)), commit=True)

SUBMISSIONS_GET_BY_ID="""
SELECT sub_id, username, timestamp, _from, _to, email_ids, subjects
FROM submissions
WHERE sub_id = "{}";
""".strip()

def submissions_get_by_id(sub_id):
    return do_sqlite3_comm(SUBMISSIONS_GET_BY_ID.format(sub_id), fetch=True)

SUBMISSIONS_GET_BY_USERNAME="""
SELECT sub_id, username, timestamp, _from, _to, email_ids, subjects
FROM submissions
WHERE user = "{}";
""".strip()

def submissions_get_by_username(username):
    return do_sqlite3_comm(SUBMISSIONS_GET_BY_ID.format(username), fetch=True)

ASSIGNMENTS_GET_BY_WEB_ID="""
SELECT web_id, email_id
FROM assignments
WHERE web_id = "{}";
""".strip()

def assignments_get_by_web_id(web_id):
    return do_sqlite3_comm(ASSIGNMENTS_GET_BY_WEB_ID.format(web_id), fetch=True)

ASSIGNMENTS_GET_BY_EMAIL_ID="""
SELECT web_id, email_id
FROM assignments
WHERE email_id = "{}";
""".strip()

def assignments_get_by_email_id(email_id):
    return do_sqlite3_comm(ASSIGNMENTS_GET_BY_EMAIL_ID.format(email_id), fetch=True)

ASSIGNMENTS_GET_ALL="""
SELECT *
FROM assignments;
""".strip()

def assignments_get_all():
    return do_sqlite3_comm(ASSIGNMENTS_GET_ALL, fetch=True)

NEWUSERS_NEW="""
INSERT VALUES username, password, student_id = ("{}","{}","{}")
INTO accounts;
""".strip()

def newusers_new(username, password, student_id):
    return do_sqlite3_comm(NEWUSERS_NEW.format(username, password, student_id), commit=True)

NEWUSERS_GET_BY_STUDENT_ID="""
SELECT registration_id, username, password
FROM newusers
WHERE student_id = "{}";
""".strip()

def newusers_get_by_student_id(student_id):
    return do_sqlite3_comm(NEWUSERS_GET_BY_STUDENT_ID.format(student_id), commit=True)

NEWUSERS_DELETE_BY_ID="""
DELETE FROM accounts
WHERE id = "{}";
""".strip()

def newusers_delete_by_registration_id(registration_id):
    return do_sqlite3_comm(NEWUSERS_DELETE_BY_ID.format(registration_id), commit=True)
