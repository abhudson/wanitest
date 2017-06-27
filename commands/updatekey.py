from common import wk_user

DESCRIPTION = u'Update your stored WaniKani key'
SORT_ID = 10


def execute(key_data, key_file=wk_user.DEFAULT_USER_FILE):
    info = wk_user.from_server(key_data)
    if not info:
        return False

    print(info.summary())
    info.save(key_file)
    return True
