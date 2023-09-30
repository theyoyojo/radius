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

SUB_GETFOR_USERNAME_ASN="""
SELECT (submission_id, student_id, assignment_id,
    submission_name, submission_grade, submission_comments)
FROM submissions
WHERE student_id = "{}"
AND assignment_id = "{}";
""".strip()
sub_getfor_username_asn = lambda dub: _get_(SUBS_GETFOR_USRASN.format(*p))

SUBS_GET="""
SELECT *
FROM submissions;
""".strip()
sub_get                 = lambda    : _get_(SUBS_GET_ALL)
                                
SES_GETBY_TOKEN="""
SELECT token, username, expiry
FROM sessions
WHERE token = "{}";
""".strip()
ses_getby_token         = lambda tok: _get_(SESSIONS_GET_BY_TOKEN.format(tok))

SES_GETBY_USERNAME="""
SELECT token, username, expiry
FROM sessions
WHERE username = "{}";
""".strip()
ses_getby_username      = lambda usn: _(SESSIONS_GET_BY_USERNAME.format(usn))

SES_INS="""
INSERT INTO sessions (token, username, expiry)
VALUES ("{}", "{}", "{}")
RETURNING username;
""".strip()
ses_ins                 = lambda tpl: _set_(SES_INS.format(*tpl))

SES_DELBY_TOKEN="""
DELETE FROM sessions
WHERE token = "{}"
RETURNING username;
""".strip()
ses_delby_token         = lambda tok: _set_(SES_DELBY_TOKEN.format(tok))

SES_DELBY_USERNAME= """
DELETE FROM sessions
WHERE username = "{}"
RETURNING username;
""".strip()
ses_delby_username      = lambda usn: _set_(SES_DELBY_USERNAME.format(usn))

SES_GET="""
SELECT id, username, pwdhash, lfx
FROM users;
""".strip()
ses_get                 = lambda    : _get_(SES_GET)

USR_PWDHASHFOR_USERNAME="""
SELECT pwdhash
FROM users
WHERE username = "{}"
""".strip()
usr_pwdhashfor_username = lambda usn: _get_(USR_GET)


USR_INS="""
INSERT INTO users (username, pwdhash, lfx, student_id)
VALUES ("{}", "{}", "{}", "{}");"
""".strip()
usr_ins =               = lambda usr: _set_(USR_INS.format(usr))

USR_GET="""
SELECT id, username, pwdhash, lfx
FROM users;
""".strip()
usr_get                 = lambda    : _get_(USR_GET)

USR_GETIF_LFX_USERNAME="""
SELECT lfx
FROM users
WHERE username = "{}";
""".strip()
usr_getif_lfx_username  = lambda usn: _get_(USR_GETIF.format(usr))

SUB_INS="""
INSERT INTO submissions (sub_id, username, timestamp, _from, _to, email_ids, subjects)
VALUES ("{}","{}","{}","{}","{}","{}","{}");
""".strip()
sub_ins                 = lambda sub: _set_(SUB_INS.format(*sub))

SUB_GETBY_SUBID="""
SELECT sub_id, username, timestamp, _from, _to, email_ids, subjects
FROM submissions
WHERE sub_id = "{}";
""".strip()
sub_getby_subid         = lambda sid: _get_(SUB_GETBY_SUBID.format(sid))

SUB_GETBY_USERNAME="""
SELECT sub_id, username, timestamp, _from, _to, email_ids, subjects
FROM submissions
WHERE user = "{}";
""".strip()
sub_getby_username      = lambda usr: _get_(SUB_GETBY_USERNAME.format(usr))

ASN_GETBY_WEBID="""
SELECT web_id, email_id
FROM assignments
WHERE web_id = "{}";
""".strip()
asn_getby_webid         = lambda wid: _get_(ASN_GETBY_WEBID.format(web_id))

ASN_GETBY_EMAILID="""
SELECT web_id, email_id
FROM assignments
WHERE email_id = "{}";
""".strip()
asn_getby_email_id     = lambda eid: _get_(ASN_GET_BY_EMAIL_ID.format(eid))

ASN_GET="""
SELECT *
FROM assignments;
""".strip()
asn_get                 = lambda: _get_(ASN_GET)

REG_INS="""
INSERT VALUES username, password, student_id = ("{}","{}","{}")
INTO accounts;
""".strip()
reg_ins                 = lambda tpl: _set_(REG_INS.format(tpl))

REG_GETBY_STUID="""
SELECT registration_id, username, password
FROM newusers
WHERE student_id = "{}";
""".strip()
reg_getby_stuid         = lambda sid: _set_(REG_GET_BY_STUDENTID.format(sid))

REG_DELBY_REGID="""
DELETE FROM accounts
WHERE id = "{}";
""".strip()
reg_delby_regid         = lambda rid: _get_(REG_DEL_BY_REGISRATION_ID.format(rid))

