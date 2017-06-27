import unittest
import os
import sys
import glob
import shutil
from tempfile import NamedTemporaryFile, mkdtemp

from common import wk_user, wk_database, ranked_lists
from util import StdReplacer

# Requires that the user file has been loaded at least once - otherwise
# there's no account to test with!
SAVED_USER = wk_user.from_file()
if SAVED_USER is None:
    sys.stderr.write(
u"""This test requires that {} exists in the current directory. Please create it
by running:
    wanitest.py updatekey <your_key>
""".format(wk_user.DEFAULT_USER_FILE))
    sys.exit(1)


class CommonCase(unittest.TestCase):
    def setUp(self):
        self.temp_filename = NamedTemporaryFile(delete=False).name
        self.temp_dirname = mkdtemp()

    def _clear_temp_directory(self):
        for root, dirs, files in os.walk(self.temp_dirname):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def tearDown(self):
        try:
            os.unlink(self.temp_filename)
        except OSError:
            # Probably already deleted
            pass
        self.assertFalse(os.path.exists(self.temp_filename))
        try:
            shutil.rmtree(self.temp_dirname)
        except OSError:
            # Probably already deleted
            pass
        self.assertFalse(os.path.exists(self.temp_dirname))


class TestData(CommonCase):
    GOOD_KEY = u'123abc123abc123abc123abc123abc12'

    def test_key_validity(self):
        self.assertTrue(wk_user._is_valid_key(self.GOOD_KEY))
        self.assertFalse(wk_user._is_valid_key(self.GOOD_KEY[:31]))  # short
        self.assertFalse(wk_user._is_valid_key(self.GOOD_KEY + '1'))  # long
        self.assertFalse(wk_user._is_valid_key(''))  # empty
        self.assertFalse(wk_user._is_valid_key(
                12345678901234567890123456789012))  # not a string
        self.assertFalse(wk_user._is_valid_key(None))    # not a string
        self.assertFalse(wk_user._is_valid_key(
                u'123abc123abc123abc123abc123abc1q'))    # bad hex

    def test_bad_user_files(self):
        os.unlink(self.temp_filename)
        self.assertFalse(os.path.exists(self.temp_filename))

        def info_from_file(data):
            with open(self.temp_filename, 'w') as f:
                f.write(data)
            with StdReplacer() as replacer:
                result = wk_user.from_file(self.temp_filename)
            os.unlink(self.temp_filename)
            return result, replacer.captured_stdout, replacer.captured_stderr

        with StdReplacer() as replacer:
            result = wk_user.from_file(self.temp_filename)
        self.assertIsNone(result)
        self.assertIn(u'No existing user data in file',
                      replacer.captured_stderr)

        result, stdout, stderr = info_from_file(u'bad data')
        self.assertIsNone(result)
        self.assertIn(u'Invalid user data in file', stderr)

        result, stdout, stderr = info_from_file(u'{"username": "abc"}')
        self.assertIsNone(result)
        self.assertIn(u'User data in file {} missing key field'.format(
                self.temp_filename), stderr)

        result, stdout, stderr = info_from_file(u'{"key": "abc"}')
        self.assertIsNone(result)
        self.assertIn(u'User data in file {} missing username field'.format(
                self.temp_filename), stderr)

        result, stdout, stderr = info_from_file(
                u'{"username": "abc", "key": "abc"}')
        self.assertIsNone(result)
        self.assertIn(u'Invalid key in file {}: {}'.format(
                self.temp_filename, 'abc'), stderr)


class TestInfo(CommonCase):
    def test_normal_flow(self):
        # Load data from server, save into new file
        server_user = wk_user.from_server(SAVED_USER.key)
        print SAVED_USER.info
        name = SAVED_USER.info[u'username']
        level = SAVED_USER.info[u'level']
        self.assertEqual(name, server_user.info[u'username'])
        self.assertTrue(server_user)
        self.assertTrue(server_user.save(self.temp_filename))

        # Load data from file again
        disk_user = wk_user.from_file(self.temp_filename)
        self.assertEqual(server_user.summary(), disk_user.summary())

        # Load the various data sections
        server_items = wk_database.WKDatabase(server_user)
        server_items.get_items()
        for itype in wk_database.WKDatabase.ITEM_TYPES:
            self.assertIn(itype, server_items._grouped_data)
            self.assertGreaterEqual(len(server_items._grouped_data[itype]),
                                    level)
        #self.assertGreater(len(server_items.criticals), 0)

        # Save and reload
        self._clear_temp_directory()
        server_items.save(self.temp_dirname)
        output_dirname = os.path.join(self.temp_dirname, name)
        self.assertTrue(os.path.exists(output_dirname))
        files = map(os.path.basename,
                    glob.glob(os.path.join(output_dirname, u'*.json')))
        for itype in wk_database.WKDatabase.ITEM_TYPES:
            for i in xrange(1, level + 1):
                self.assertIn(u'{}_{:02}.json'.format(itype, i), files)
        self.assertIn(u'criticals.json', files)
        disk_items = wk_database.WKDatabase(server_user)
        disk_items.load(self.temp_dirname)
        #self.assertEqual(server_items, disk_items)


class TestRankings(unittest.TestCase):
    def test_normal_flow(self):
        # Assumes that standard data has already been loaded
        user = wk_user.from_file()
        items = wk_database.WKDatabase(user)
        items.load()
        rankings = ranked_lists.RankedLists(wk_database)

if __name__ == '__main__':
    unittest.main()
