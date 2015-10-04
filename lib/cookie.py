__author__ = 'yura'

import hmac
import random
from string import letters

SALT = 'abCmiLbRhqNehGPjQeix'


def _make_hash_string(s, salt=None):
    """
    Make a hash from stirng and return it as stirng

    param s: <str>
        String that will be hashed
    param salt: <str>
        Salt for hash
    return: <tuple>
        hash string, salt
    """
    if not salt:
        salt = ''.join([random.choice(letters) for _ in range(20)])
    hmac_obj = hmac.new(salt, s)
    return hmac_obj.hexdigest(), salt


def make_token_cookie(user_id, salt=SALT):
    """
    Make a cookie token

    param user_id: <str>
        user_id
    return: <str>
        cookie stirng "user_id|hash|salt"
    """
    token, salt = _make_hash_string(str(user_id), salt)
    return '%s|%s|%s' % (user_id, token, salt)


def verify_token(token):
    """
    Check if token is valid, return token or None

    param token: <str>
        token
    return: <bool>
        user id  or None
    """
    token = str(token)
    if not token:
        return False
    user_id, t_hash, t_salt = token.split('|')
    return user_id if token == make_token_cookie(user_id=user_id, salt=t_salt) else None

