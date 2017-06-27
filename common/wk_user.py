import os
import sys
import json

from crabigator.wanikani import WaniKani, WaniKaniError

import util

DEFAULT_USER_FILE = os.path.join(os.path.abspath('.'), u'wanikani_user.json')


class BadKeyError(Exception):
    def __init__(self, message, key):
        super(BadKeyError, self).__init__(message)
        self.key = key

    def __str__(self):
        return u'Key: {}; Message: {}'.format(self.key, self.message)


class BadInfoError(Exception):
    def __init__(self, message):
        super(BadInfoError, self).__init__(message)

# Cached since application was loaded
__wanikani_apis = {}


def _get_api_by_key(key_data):
    """Get a WaniKani API object using the given key"""
    api = __wanikani_apis.get(key_data)
    if api:
        return api

    api = __wanikani_apis[key_data] = WaniKani(key_data)
    return api


def _is_valid_key(key):
    if not (key and isinstance(key, basestring)):
        return False
    if len(key) != 32:
        return False
    try:
        int(key, 16)
    except ValueError:
        return False
    return True


def from_file(filename=DEFAULT_USER_FILE):
    try:
        with open(filename) as f:
            info = json.load(f)
    except IOError:
        sys.stderr.write(
            u'No existing user data in file {}\n'.format(filename))
        return None
    except ValueError:
        sys.stderr.write(
            u'Invalid user data in file {}\n'.format(filename))
        return None

    try:
        key = info.pop('key')
    except KeyError:
        sys.stderr.write(
            u'User data in file {} missing key field.\n'.format(filename))
        return None

    try:
        info[u'username']
    except KeyError:
        sys.stderr.write(u'User data in file {} missing username field.\n'
                         .format(filename))
        return None

    try:
        return _WKUserInfo(key, info)
    except BadKeyError as e:
        sys.stderr.write(u'{} in file {}: {}\n'.format(
                e.message, filename, e.key))
        return None


def from_server(key):
    if not _is_valid_key(key):
        sys.stderr.write(u'Invalid key format: {}\n'.format(key))
        return None
    api = _get_api_by_key(key)
    try:
        info = api.user_information.__dict__
    except WaniKaniError as e:
        sys.stderr.write(
            u'Key {} not authorised by server: {}\n'.format(key, e.message))
        return None

    # Should not be possible to get a BadKeyError here
    return _WKUserInfo(key, info)


class _WKUserInfo(object):

    def __init__(self, key, info):
        if not _is_valid_key(key):
            raise BadKeyError(u'Invalid key', key)
        self.key = key
        if not info:
            raise WaniKaniError(key, '')
        self.info = info.copy()
        util.clean_dictionary_dates(self.info)
        self.api = _get_api_by_key(key)

    def save(self, filename=DEFAULT_USER_FILE):
        if os.path.exists(filename):
            print u'Overwriting existing file at {}'.format(filename)
        to_write = self.info.copy()
        to_write[u'key'] = self.key
        with open(filename, 'w') as f:
            json.dump(to_write, f)
        print u'Key "{}" for {} saved to {}'.format(self.key,
                                                   to_write[u'username'],
                                                   filename)
        return True

    def summary(self):
        lines = [u'Details for {}:'.format(self.key)]
        to_print = self.info.copy()
        lines.append(u'- username: {}'.format(to_print.pop(u'username')))
        for field, value in sorted(to_print.iteritems()):
            lines.append(u'- {}: {}'.format(field, value))
        return '\n'.join(lines)
