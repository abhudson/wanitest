def join_items(items):
    return u'\n'.join(map(unicode, items))


class WKItem(object):
    def __init__(self, data):
        self.data = data.copy()
        self.item_type = u'unknown'
        self.data[u'initial'] = u'U'
        if data.get(u'user_specific') is None:
            data[u'user_specific'] = {}
        self.data[u'meaning_str'] = self._join_lists(self.data[u'meaning'],
                                data[u'user_specific'].get(u'user_synonyms'))
        self.data[u'url'] = self.url

    def __getitem__(self, item):
        return self.data[u'user_specific'][item]

    def _join_lists(self, *lists):
        combined = []
        for each in lists:
            combined.extend(each or [])
        return u', '.join(combined)

    @property
    def url(self):
        return u'https://www.wanikani.com/{}/{}'.format(self.item_type,
                                                        self.data[u'character'])
    # def __str__(self):
    #     return self.__unicode__()


class Radical(WKItem):
    """ {u'character': u'\u5de5',
  u'image': None,
  u'level': 1,
  u'meaning': [u'construction'],
  u'user_specific': {u'available_date': u'1499036400',
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
                     u'user_synonyms': None}}]
    """
    # {'meaning': [u'seven'], 'type': u'radical', 'level': 1,
    #  'user_specific': None, 'image': None, 'character': u'\u4e03',
    #  'percentage': 89}
    def __init__(self, item):
        super(Radical, self).__init__(item)
        self.item_type = u'radicals'
        self.data[u'initial'] = u'R'

    def __unicode__(self):
        return u"""{initial} {character}: {meaning_str}""".format(**self.data)


class Kanji(WKItem):
    """
{u'character': u'\u5de5',
u'important_reading': u'onyomi',
u'kunyomi': None,
u'level': 1,
u'meaning': [u'construction', u'industry'],
u'nanori': None,
u'onyomi': [u'\u3053\u3046', u'\u304f'],
u'user_specific': {u'available_date': u'1499209200',
                 u'burned': False,
                 u'burned_date': u'-36000',
                 u'meaning_correct': 7,
                 u'meaning_current_streak': 7,
                 u'meaning_incorrect': 0,
                 u'meaning_max_streak': 7,
                 u'meaning_note': None,
                 u'reading_correct': 7,
                 u'reading_current_streak': 7,
                 u'reading_incorrect': 0,
                 u'reading_max_streak': 7,
                 u'reading_note': None,
                 u'srs': u'enlighten',
                 u'srs_numeric': 8,
                 u'unlocked_date': u'1484266068',
                 u'user_synonyms': None}}]
    """

    def __init__(self, item):
        super(Kanji, self).__init__(item)
        self.item_type = u'kanji'
        self.data[u'initial'] = u'K'
        self.data[u'unimportant_reading'] = self.__opposite(
                                self.data[u'important_reading'])
        self.data[u'reading'] = self._join_lists(
                                self.data[self.data[u'important_reading']])
        self.data[u'other'] = self._join_lists(
                                self.data[self.data[u'unimportant_reading']])

    def __opposite(self, reading):
        return u'onyomi' if reading == u'kunyomi' else u'kunyomi'

    def __unicode__(self):
        result = u"""{initial} {character}: {reading} ({important_reading})
    - {meaning_str}""".format(**self.data)
        if self.data['other'] and self.data['other'] != [u'None']:
            result += u"""
    - {other}: {unimportant_reading}""".format(**self.data)
        return result


class Vocabulary(WKItem):
    """{u'character': u'\u4eba\u5de5',
     u'kana': [u'\u3058\u3093\u3053\u3046'],
     u'level': 1,
     u'meaning': [u'artificial',
                  u'man made',
                  u'human made',
                  u'human work',
                  u'human skill'],
     u'user_specific': {u'available_date': u'1499637600',
                        u'burned': False,
                        u'burned_date': u'-36000',
                        u'meaning_correct': 13,
                        u'meaning_current_streak': 10,
                        u'meaning_incorrect': 1,
                        u'meaning_max_streak': 10,
                        u'meaning_note': None,
                        u'reading_correct': 13,
                        u'reading_current_streak': 8,
                        u'reading_incorrect': 2,
                        u'reading_max_streak': 8,
                        u'reading_note': None,
                        u'srs': u'enlighten',
                        u'srs_numeric': 8,
                        u'unlocked_date': u'1484479585',
                        u'user_synonyms': None}}]
    """

    def __init__(self, item):
        super(Vocabulary, self).__init__(item)
        self.item_type = u'vocabulary'
        self.data[u'initial'] = u'V'
        self.data[u'kana'] = self._join_lists(self.data[u'kana'])

    def __unicode__(self):
        return u"""{initial} {character}: {kana}
    - {meaning_str}""".format(**self.data)


def get_item(item_type, item):
    if item_type in (u'radicals', u'radical') :
        return Radical(item)
    elif item_type == u'kanji':
        return Kanji(item)
    elif item_type == u'vocabulary':
        return Vocabulary(item)
    return None
