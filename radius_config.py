#!/bin/env python3
#
# radius_config.py: configuration and constant definition

class radius_config:
    APPLICATION     = 'radius'
    VERSION         = '0.1'
    SOURCE          = 'https://github.com/underground-software/radius'

    # read these documents from a filesystem path
    PATH_LOCAL_ROOT=  f'{os.environ.get("ORBIT_PREFIX")}{os.environ.get("ORBIT_HOST")}'
    # TODO: this will become /var/orbit/databse/orbit.db or something
    PATH_LOCAL_DATABASE = 'orbit.db'

    # make exernal GET request to find these documents
    PATH_GET_LOGO       = '/kdlp.png'
    PATH_GET_STYLE      = '/style.css'

    MINS_SESSION= 180
    NAV_BUTTONS = [
        (       '/index.md', 'Home'     ),
        ('/course/index.md', 'Course'   ),
        (          '/login', 'Login'    ),
        (       '/register', 'Register' ),
        (      '/dashboard', 'Dashboard'),
        (         '/who.md', 'Who'      ),
        (        '/info.md', 'Info'     ),
        (           '/cgit', 'Git'      )]:
