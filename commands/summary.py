from common import wk_user

DESCRIPTION = 'Print the summary of the stored WaniKani key'
SORT_ID = 40


def execute(info_file=wk_user.DEFAULT_USER_FILE):
    info = wk_user.from_file(info_file)
    if not info:
        return False

    print info.summary()
    return True
