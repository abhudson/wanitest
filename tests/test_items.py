import unittest
import os
import glob
import shutil
from tempfile import NamedTemporaryFile, mkdtemp

from common import wk_user, wk_database, ranked_lists
from util import StdReplacer


class TestRadical(unittest.TestCase):
    SAMPLE = {
        u'character': u'\u5de5',
        u'image': None,
        u'level': 1,
        u'meaning': [u'construction'],
        u'user_specific': {
            u'available_date': u'1499036400',
            u'burned': False,
            u'burned_date': u'-36000',
            u'meaning_correct': 7,
            u'meaning_current_streak': 7,
            u'meaning_incorrect': 0,
            u'meaning_max_streak': 7,
            u'meaning_note': None,
            u'reading_correct': None,
            u'reading_current_streak': None,
            u'reading_incorrect': None,
            u'reading_max_streak': None,
            u'reading_note': None,
            u'srs': u'enlighten',
            u'srs_numeric': 8,
            u'unlocked_date': u'1483894582',
            u'user_synonyms': None
        }
    }

    def test_good(self):
        pass


class TestKanji(unittest.TestCase):
    def test_good(self):
        pass


class TestVocabulary(unittest.TestCase):
    def test_good(self):
        pass

if __name__ == '__main__':
    unittest.main()
