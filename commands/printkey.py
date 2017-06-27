from common import wk_user

DESCRIPTION = u'Print the currently stored WaniKani key'
SORT_ID = 15


def execute(info_file=wk_user.DEFAULT_USER_FILE):
    key_data = wk_user.from_file(info_file)
    if key_data is not None:
        print key_data.key
    return True
