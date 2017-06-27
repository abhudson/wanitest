import os
import json
import glob
from collections import defaultdict

from common.wk_item import get_item
import util


class WKDatabase(object):
    """
    Representation of the Wanikani user-specific database. Contains all of the
    radicals/kanji/vocabulary they know, along with their success rates and
    critical items.
    """
    ITEM_TYPES = [u'radicals', u'kanji', u'vocabulary']

    def __init__(self, user_info):
        self.api = user_info.api
        self.user_info = user_info
        self._grouped_data = {}
        self._criticals = []
        self.combined_items = {}
        self.critical_items = []

    def __get_user_directory(self, base_directory):
        if base_directory is None:
            base_directory = os.path.abspath('.')

        username = self.user_info.info[u'username']
        user_directory = os.path.join(base_directory, username)
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)
            print u'Created data directory {}'.format(user_directory)
        return user_directory

    def __combine_data(self):
        for prefix, level_data in self._grouped_data.iteritems():
            for level, item_list in level_data.iteritems():
                for item in item_list:
                    key = (prefix, item[u'character'])
                    self.combined_items[key] = get_item(prefix, item)

    def __build_criticals(self):
        self.critical_items = [get_item(x[u'type'], x) for x in self._criticals]

    @staticmethod
    def __wanikani_to_json(item, keep_all=False):
        json_item = item.__dict__.copy()

        # If it hasn't been seen, it doesn't have user specific data
        if not (keep_all or item.user_specific):
            return None

        try:
            json_item[u'user_specific'] = item.user_specific.__dict__.copy()
            # library converts to datetime objects, which don't serialise!
            util.clean_dictionary_dates(json_item[u'user_specific'])
        except AttributeError:
            pass

        return json_item

    def get_items(self):
        for prefix in self.ITEM_TYPES:
            print u'Processing', prefix
            fn = getattr(self.api, u'get_{}'.format(prefix))

            data = self._grouped_data[prefix] = defaultdict(list)
            for item in fn():
                json_item = self.__wanikani_to_json(item)
                if not json_item:
                    continue
                data[item.level].append(json_item)

        self.__combine_data()

    def get_criticals(self, critical_ratio=90):
        print u'Processing criticals'
        raw_criticals = self.api.get_critical_items(percent=critical_ratio)
        # Don't consider the current level to be critical
        level = self.user_info.info[u'level']
        self._criticals = filter(None, [self.__wanikani_to_json(x, True)
                                        for x in raw_criticals
                                        if x.level != level])
        self.__build_criticals()

    def save(self, data_directory=None):
        user_directory = self.__get_user_directory(data_directory)
        for prefix, subdata in self._grouped_data.iteritems():
            for level, data in subdata.iteritems():
                filename = os.path.join(user_directory, u'{}_{:02}.json'.format(
                    prefix, level))
                with open(filename, 'w') as f:
                    json.dump(data, f)

        filename = os.path.join(user_directory, u'criticals.json')
        with open(filename, 'w') as f:
            json.dump(self._criticals, f)

    def load(self, data_directory=None):
        user_directory = self.__get_user_directory(data_directory)
        self._grouped_data = defaultdict(dict)

        for data_file in glob.glob(os.path.join(user_directory, u'*.json')):
            base = os.path.basename(data_file[:-len(u'.json')])
            try:
                prefix, level = base.split('_')
                level = int(level)
            except ValueError:
                continue
            if prefix not in self.ITEM_TYPES:
                continue
            if level < 1 or level > self.user_info.info[u'level']:
                continue

            with open(data_file) as f:
                self._grouped_data[prefix][level] = json.load(f)

        filename = os.path.join(user_directory, u'criticals.json')
        with open(filename, 'r') as f:
            self._criticals = json.load(f)

        self.__combine_data()
        self.__build_criticals()
