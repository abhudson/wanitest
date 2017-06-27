from common import wk_user
from commands import summary

DESCRIPTION = u'Check the stored WaniKani key against the server and print ' \
              'its details'
SORT_ID = 20


def execute(info_file=wk_user.DEFAULT_USER_FILE):
    result = summary.execute(info_file)
    print u'Key is {}valid.'.format(u'' if result else u'in')
    return True