from common import wk_words
from common.wk_item import join_items
import util

DESCRIPTION = u'Display a selection of words'
SORT_ID = 70


def execute(word_or_count=10):
    word = ''
    count = 0
    try:
        count = int(word_or_count)
    except ValueError:
        word = word_or_count

    db = util.load_default_database()
    if not db:
        return False
    grabber = wk_words.Words(db)
    if word:
        selection = grabber.get_matches(word)
    else:
        selection = grabber.get_random(count)

    for word, item_set in selection.iteritems():
        print u'*** {} ***'.format(word)
        print join_items(item_set)
        print
    return True
