from common import wk_user, wk_database

DESCRIPTION = u'Update the stored data used in tests'
SORT_ID = 30


def execute(info_file=wk_user.DEFAULT_USER_FILE, data_directory=None):
    current_info = wk_user.from_file(info_file)
    new_info = wk_user.from_server(current_info.key)
    data = wk_database.WKDatabase(new_info)
    data.get_items()
    data.get_criticals()
    new_info.save()
    data.save(data_directory)
    return True

