class RankedLists(object):
    def __init__(self, item_info):
        self.all_items = item_info.combined_items
        self.criticals = item_info.critical_items
        self.reading_mistakes = []
        self.meaning_mistakes = []
        self.mistakes = []
        self.reading_ratio = []
        self.meaning_ratio = []

        self.__build(self.reading_mistakes, [u'reading_incorrect'])
        self.__build(self.meaning_mistakes, [u'meaning_incorrect'])
        self.__build(self.mistakes, [u'meaning_incorrect',
                                     u'reading_incorrect'])

    def __build(self, dataset, categories, reverse=True):
        total = lambda data: sum(data[c] or 0 for c in categories)
        dataset.extend([(total(data), key)
                        for key, data in self.all_items.iteritems()
                        if total(data)])
        dataset.sort(reverse=reverse)

    def get_top_reading_mistakes(self, count):
        return [self.all_items[key[1]] for key in self.reading_mistakes[:count]]

    def get_top_meaning_mistakes(self, count):
        return [self.all_items[key[1]] for key in self.meaning_mistakes[:count]]

    def get_top_mistakes(self, count):
        return [self.all_items[key[1]] for key in self.mistakes[:count]]

    def get_top_critical(self, count):
        return self.criticals[:count]

