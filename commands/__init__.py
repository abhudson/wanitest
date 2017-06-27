from collections import OrderedDict
import pkgutil


def _get_commands():
    """
    Loads all the command modules from the commands subpackage, then registers
    them so that they can be called.
    """
    unsorted_commands = []

    for instance, name, is_package in pkgutil.iter_modules([__name__]):
        x = instance.find_module(name)
        instance = x.load_module(name)
        command = getattr(instance, u'execute', None)
        if not is_package and command:
            description = getattr(instance, u'DESCRIPTION', u'No description')
            sort_id = getattr(instance, u'SORT_ID', u'')
            unsorted_commands.append((sort_id, name, command, description))

    sorted_commands = OrderedDict()
    for _, name, command, description in sorted(unsorted_commands):
        sorted_commands[name] = (command, description)
    return sorted_commands

COMMANDS = _get_commands()