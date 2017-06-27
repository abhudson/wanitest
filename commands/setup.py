from common import wk_user
from commands import updatekey, updatedata

DESCRIPTION = 'Set up your WaniKani test experience. Do this first!'
SORT_ID = 5


def execute(key_data, key_file=wk_user.DEFAULT_USER_FILE, data_directory=None):
    return (
        updatekey.execute(key_data, key_file) and
        updatedata.execute(key_file, data_directory)
    )
