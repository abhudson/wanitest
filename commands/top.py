import sys

from common import wk_user, wk_database, ranked_lists
from common.wk_item import join_items
import util

DESCRIPTION = u'Display the information about the top mistakes'
SORT_ID = 60

CATEGORIES = (u'reading_mistakes', u'meaning_mistakes', u'mistakes',
              u'critical')


def execute(category, count=20):
    if category not in CATEGORIES:
        sys.stderr.write(u'Category must be one of: {}\n'.format(
                    ', '.join(CATEGORIES)))
        return False

    try:
        count = int(count)
    except ValueError:
        sys.stderr.write(u'Invalid integer: {}\n'.format(count))
        return False

    db = util.load_default_database()
    if not db:
        return False
    ranked = ranked_lists.RankedLists(db)
    fn = getattr(ranked, u'get_top_{}'.format(category))
    top_items = fn(count)

    print join_items(top_items)
    return True