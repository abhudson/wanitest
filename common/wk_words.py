from collections import defaultdict
import random


class Words(object):
    """
    Takes collections of items and generates word -> item mappings, so that
    one can test their ability to generate kanji!
    """

    def __init__(self, item_info):
        self.items = defaultdict(set)
        for key, item in item_info.combined_items.iteritems():
            if key[0] == u'radicals':
                # Can't type radicals, so pointless in a reverse exercise
                continue
            synonyms = item[u'user_synonyms'] or []
            for meaning in item.data[u'meaning'] + synonyms:
                self.items[meaning.lower()].add(item)
        self.english_words = self.items.keys()

    def get_random(self, count):
        selection = random.sample(self.english_words, count)
        return {word: self.items[word] for word in selection}

    def get_matches(self, word):
        selection = filter(lambda x: word in x, self.english_words)
        return {word: self.items[word] for word in selection}

