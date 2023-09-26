#!/bin/env python

import datetime


from orbit import ROOT, messageblock, appver, \
    get_authorized_user, AUTH_SERVER, table, DP, bytes8

import sql

from isis import isis

def build_assignments_list():
    res = []
    with open('assignments.list' ,'r') as f:
        for line in f:
            # comment
            if line[0] == '#':
                continue
            res += (line.split(' '))
    return res

def make_assignment_table(foobar):
   return table([('Grade', 'Comments', 'Time Recieved')])

def build_assignment_table(sub, assignment_name):
    dt = "-"
    if sub and sub.date:
        dt = datetime.datetime.fromtimestamp(sub.date).strftime("%Y-%m-%d %H:%M:%S")

    return ASSIGNMENT_TABLE_TEMPLATE % (assignment_name, or_dash(sub.grade), or_dash(sub.comments), dt)

def get_assignment_list():
    return sql.grades_db_exec(sql.ASSIGNMENTS_GET_ALL)

def get_latest_submission(sid, assignment_id):
    tuple_list = sql.grades_db_exec(sql.SUBMISSIONS_GET_STUDENT_ASSIGNMENT.format(sid, assignment_id))
    if tuple_list:
        return Submission(tuple_list[0])
    return None

def old_build_page(sid):
    for assignment in build_assignments_list():
        print(assignment)

    page = "<h1>Student Dashboard</h1><br>"

    page += "<code>\n"
    #page += str(get_assignment_list()[0])
    page = make_assignment_table(1)
    page += "</code>\n"

    return page

REFRESH_INTERVAL=2
def build_page(user, sid, path):
    return isis(user)

def get_id_by_user(user):
    # TODO
    return 45

def gather_id(env):

    user = get_authorized_user(AUTH_SERVER, env)
    if user is None:
        return (None, None, None)
    user = user.lower()
    DEBUG(f'new login by: {user}')

    # TODO
    sid = get_id_by_user(user)

    DEBUG(f'found student id: {sid}')

    return (user, sid, path)
