# -*- coding: utf-8 -*-

import argparse
import sys
from cStringIO import StringIO

# The crabigator API doesn't get all the available fields - so insert the ones
# that we need. There's probably a better place for this than in util, but it
# needs to be called by the main application and the tests.
from crabigator import wanikani
wanikani.RADICAL.append(('percentage', lambda x: int(x)))
wanikani.RADICAL.append(('type', lambda x: x))
wanikani.KANJI.append(('percentage', lambda x: int(x)))
wanikani.KANJI.append(('type', lambda x: x))
wanikani.VOCABULARY.append(('percentage', lambda x: int(x)))
wanikani.VOCABULARY.append(('type', lambda x: x))


def get_argument_parser():
    """Returns the argument parser with attached help information"""
    import commands
    parser = argparse.ArgumentParser(
        description=u'Extra tests for your current WaniKani level! 頑張って!',
        epilog=u'If in doubt, run "%(prog)s help"')
    parser.add_argument('command', choices=commands.COMMANDS.keys())
    parser.add_argument('arguments', nargs='*',
                        help='command-specific arguments')
    return parser


def load_default_database():
    """Grabs the default DB files based upon the default user settings file"""
    from common import wk_user, wk_database
    users = wk_user.from_file()
    if not users:
        return None
    db = wk_database.WKDatabase(users)
    if not db:
        return None
    db.load()
    return db


def clean_dictionary_dates(data):
    """Replace the dictionary's dates with something that will serialise"""
    for field, value in data.iteritems():
        try:
            data[field] = value.strftime('%s')
        except AttributeError:
            pass


class StdReplacer(object):
    """Encapsulates std(in|out|err), primarily for testing"""

    def __init__(self, content=''):
        self.content = content

    def __enter__(self):
        sys.stdin = StringIO(self.content)
        self.captured_stdout = ''
        self.captured_stderr = ''
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdin.close()
        sys.stdin = sys.__stdin__

        sys.stdout.seek(0)
        self.captured_stdout = sys.stdout.read()
        sys.stdout.close()
        sys.stdout = sys.__stdout__

        sys.stderr.seek(0)
        self.captured_stderr = sys.stderr.read()
        sys.stderr.close()
        sys.stderr = sys.__stderr__
