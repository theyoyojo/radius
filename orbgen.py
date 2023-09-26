def h(v, c):
    return f'<h{v}>{c}</h{v}'

def h1(c):
    return h(1, c)

def h2(c):
    return h(2, c)

def h3(c):
    return h(3, c)

def h4(c):
    return h(4, c)

def h5(c):
    return h(5, c)

def t_i(i):
    return ''.join(['\t' for x in range(i)])

def o(i, c):
    return f'{t_i(i)}{c}\n'

def ooo(i, c, d, e, j=0):
    return f'{o(i, c)}{o(i+j, d)}{o(i, e)}'

def oOo(i, c, d, e):
    return ooo(i, c, d, e, j=1)

def oxo(i, c, d, e):
    return f'{o(i, c)}{d}{o(i, e)}'

def table_data(c, h=False, i=0):
    d = 'd'
    if h:
        d = 'h'
    a, b = f'<t{d}>', f'</t{d}'
    return oOo(i, a, c, b)

def table_row(c, h=False, i=0):
    d = ''.join([table_data(d, h=h, i=i+1) for d in c])
    return oxo(i, '<tr>', d, '</tr>')

def table(c, i=0):
    t=''
    h=True
    for r in c:
        t += table_row(r, h, i=i+1)
        h=False
    return oxo(i, '<table>', t, '</table>')

def div(attr="", c="", i=0):
    return oxo(i, f'<div{attr}>', c, '</div>')

def li(c):
    return o(c)

def ul(c, i=0):
    return oxo(i, f'<ul>', '\n'.join([li(_li) for _li in c]), '</ul>')

def a(text, href):
    return f'<a href="{href}">{text}</a>'

def button(c, i=0, a=''):
    return oOo(i, f'<button {a}>', c, '</button>')

def input_(attr=''):
    return f'<input {attr} >'

def label(attr='', c=''):
    return f'<label {attr} >{c}</label>'

def form(attr, c):
    return f'<form {attr} >{c} </form>'


def form_login():
    return form(' id="login" method="post" action="/login" ',
        label(' for="username" ', 'Username: <br />') + \
        input_(' name="username" type="text" id="username" ') + \
        '<br />' + \
        label(' for="username" ', 'Username: <br />') + \
        input_(' name="password" type="password" id="password" ') + \
        '<br />' + \
        button('Submit', 0, ' type="submit" '))

def cookie_info_table(session):
    return table([
        ('Cookie Key', 'Value'),
        ('Token', session.token),
        ('User', session.username),
        ('Expiry', session.expiry_fmt),
        ('Remaining Validity', session.remaining_validity)])

def logout_buttons():
    return form(' id="logout" method="get" action="/login" ', \
        input_(' type="hidden" name="logout" value="true" ') + \
        button('Logout', 0, ' type="submit" class="logout" ')) + \
        form(' id="rewnew" method="get" action="/login" ',
        input_(' id="renew" method="get" action="/" ') + \
        button('Renew', 0, ' type="submit" class="renew" '))

def form_authorized(session):
    return div(' class="logout_ifo" ', div(' class="logout_left" ', gen_cookie_info_table(session)) + \
        div(' class="logout_right" ',
            div(' class="logout_right_inner" ', h5("Welcome!") + ul([a('Dashboard', '/dashboard')]))))  + \
        div(gen_logout_buttons() ,' class="logout_buttons" ')

def form_register():
    return form(' id="register" method="post" action="/register" ',
            label(' for="student_id" ','Student ID:') + \
            input_(' name="student_id" type="text" id="student_id" ') + \
            '<br />' + \
            button('Submit', ' type="submid" '))
