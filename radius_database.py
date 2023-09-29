#!/usr/bin/env python

import sqlite, radius

# <shorthand> => <sql_table_name>
# USR => users
# ASN => assignments
# SUB => submissions
# REG => newusers

def _sqlite3(command, _set=False, _get=False):
    result=None
    db_con = sqlite3.connect(radius.config.PATH_LOCAL_DATABASE)
    db_cur0 = db_con.cursor()
    db_cur1 = db_cur0.execute(command)
    if _get:
        result=db_cur1.fetchall()
    if _set:
        db_cur2 = db_cur1.execute("COMMIT;")
    db_con.close()
    return result
_set_ = lambda c: _sqlite3(c, _set=(True)
_get_ = lambda c: _sqlite3(c, _get=True)

SUB_GETFOR_USER="""
SELECT (submission_id, student_id, assignment_id,
    submission_name, submission_grade, submission_comments)
FROM submissions
WHERE student_id = "{}"
AND assignment_id = "{}";
""".strip()
sub_getfor_user = lambda dub: _get_(SUBS_GET_BY_STUDENT_AND_ASSIGNMENT.format(*p))

SUBS_GET="""
SELECT *
FROM submissions;
""".strip()
sub_get                          = lambda    : _get_(SUBS_GET_ALL)
                                
SES_GETBY_TOKEN="""
SELECT token, username, expiry
FROM sessions
WHERE token = "{}";
""".strip()
ses_getby_token                  = lambda tok: _get_(SESSIONS_GET_BY_TOKEN.format(tok))

SES_GETBY_USERNAME="""
SELECT token, username, expiry
FROM sessions
WHERE username = "{}";
""".strip()
ses_getby_username               = lambda usr: _(SESSIONS_GET_BY_USERNAME.format(usr))

SES_INS="""
INSERT INTO sessions (token, username, expiry)
VALUES ("{}", "{}", "{}")
RETURNING username;
""".strip()
ses_ins                           = lambda tpl: _set_(SES_INS.format(*tpl))

SES_DELBY_TOKEN="""
DELETE FROM sessions
WHERE token = "{}"
RETURNING username;
""".strip()
ses_delby_token                   = lambda t: do_sqlite3_comm(SESSIONS_DELETE_BY_USER.format()t, _set=True)

SESSIONS_DELETE_BY_USERNAME= """
DELETE FROM sessions
WHERE username = "{}"
RETURNING username;
""".strip()
sessions_delete_by_username = lambda s: do_sqlite3_comm(SESSIONS_DELETE_BY_USERNAME.format(u), _set=True)

SESSIONS_GET_ALL="""
SELECT id, username, pwdhash, lfx
FROM users;
""".strip()
sessions_get_all = do_sqlite

def sessions_get_all():
    return do_sqlite3_comm(SESSIONS_GET_ALL, _get=True)

USR_GET_PWDHASH_BY_USERNAME="""
SELECT pwdhash
FROM users
WHERE username = "{}"
""".strip()

def users_get_pwdhash_by_username(u):
    return do_sqlite3_comm(USERS_GET_PWDHASH.format(u), _get=True)

USERS_NEW="""
INSERT INTO users (username, pwdhash, lfx, student_id)
VALUES ("{}", "{}", "{}", "{}");"
""".strip()

def users_new(u, p, l=False, i=0):
    return do_sqlite3_comm(USERS_GET_PWDHASH_COMM.format(u, p, l, i), _set=True)

USERS_GET_ALL="""
SELECT id, username, pwdhash, lfx
FROM users;
""".strip()

def sessions_get_all():
    return do_sqlite3_comm(USERS_GET_ALL, _get=True)

USERS_GET_LFX_BY_USERNAME="""
SELECT lfx
FROM users
WHERE username = "{}";
""".strip()

def users_get_lfx_by_username(u):
    return do_sqlite3_comm(USERS_GET_LFX_BY_USERNAME.format(u), _get=True)

SUB_INS="""
INSERT INTO submissions (sub_id, username, timestamp, _from, _to, email_ids, subjects)
VALUES ("{}","{}","{}","{}","{}","{}","{}");
""".strip()
sub_insert          =   lambda sub: b

def sub_insert(sub_id, username, timestamp, from_, to_, email_ids, subjects):
    return do_sqlite3_comm(SUBS_INSERT.format(sub_id, user, time,
        from_, to_, "\n".join(email_ids), "\n".join(subjects)), _set=True)

SUB_GET_BY_SUBID="""
SELECT sub_id, username, timestamp, _from, _to, email_ids, subjects
FROM submissions
WHERE sub_id = "{}";
""".strip()

def sub_get_by_id(sub_id):
    return do_sqlite3_comm(SUBS_GET_BY_ID.format(sub_id), _get=True)

SUB_GET_BY_USERNAME="""
SELECT sub_id, username, timestamp, _from, _to, email_ids, subjects
FROM submissions
WHERE user = "{}";
""".strip()
sub_get

def sub_get_by_username(username):
    return do_sqlite3_comm(SUBS_GET_BY_ID.format(username), _get=True)

ASSIGNMENTS_GET_BY_WEB_ID="""
SELECT web_id, email_id
FROM assignments
WHERE web_id = "{}";
""".strip()
asn_get_by_web_id     = lambda _get_(ASSIGNMENTS_GET_BY_WEB_ID.format(web_id), _get=True)

ASN_GET_BY_EMAIL_ID="""
SELECT web_id, email_id
FROM assignments
WHERE email_id = "{}";
""".strip()
asn_get_by_email_id   = lambda eid: _get_(ASN_GET_BY_EMAIL_ID.format(eid))

ASSIGNMENTS_GET_ALL="""
SELECT *
FROM assignments;
""".strip()
asn_get               = lambda: _get_(ASN_GET_ALL)

REG_INS="""
INSERT VALUES username, password, student_id = ("{}","{}","{}")
INTO accounts;
""".strip()
reg_ins               = lambda tpl: _set_(REG_INS.format(tpl))

REG_GET_BY_STUDENTID="""
SELECT registration_id, username, password
FROM newusers
WHERE student_id = "{}";
""".strip()
reg_getby_studentid  = lambda sid: _set_(REG_GET_BY_STUDENTID.format(sid))

REG_DEL_BY_REGISTRATION_ID="""
DELETE FROM accounts
WHERE id = "{}";
""".strip()
reg_delby_registrationid = lambda rid: _get_(REG_DEL_BY_REGISRATION_ID.format(rid))

