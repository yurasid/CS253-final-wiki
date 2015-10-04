__author__ = 'yura'

import re

# ======================
# Form input validation
# ======================

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PASS_RE = re.compile(r"^.{3,20}$")


def validation_form(username=None, password=None,
                    email=None, verify=None):
    """
    Validate data from user signup and login forms

    :param username:
    :param password:
    :param email:
    :param verify:
    :return: <dict>
        dict with errors or None
    """

    params = dict()

    if not valid_username(username):
        params['error_username'] = 'Login too short. Min 3 char, max 20 char'

    if not valid_password(password):
        params['error_password'] = 'Password too short. Min 3 char, max 20 char'

    if verify != password:
        params['error_verify'] = 'Password and verify is different'

    if not valid_email(email):
        params['error_email'] = 'Email is invalid. You can leave email blank'

    return None if len(params) == 0 else params


def valid_username(u):
    """
    Return user if user is valid None otherwise

    :param u: <str>
        user
    :return: <bool>
        T of F
    """
    return u and USER_RE.match(u)


def valid_password(p):
    return p and PASS_RE.match(p)


def valid_email(e):
    return EMAIL_RE.match(e) or not e


