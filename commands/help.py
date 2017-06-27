import sys
from inspect import getargspec

DESCRIPTION = u'Prints the help information for all the commands'
SORT_ID = 0


def execute(command=None):
    import commands
    if command:
        try:
            fn, description = commands.COMMANDS[command]
        except KeyError:
            sys.stderr.write(u'Command not found: {}\n'.format(command))
            return False

        output = u"""Command:\t{}
Description:\t{}
Arguments:{}"""
        # ignore *args and **kwargs unless we start using them
        arg_names, _, _, arg_defaults = getargspec(fn)
        if arg_names:
            arg_lines = []
            arg_defaults = list(arg_defaults)
            for name in reversed(arg_names):
                curr_default = u' (required)'
                if arg_defaults:
                    curr_default = u' (default: {})'.format(arg_defaults.pop())
                arg_lines.insert(0, u'- {}{}'.format(name, curr_default))
            arg_lines.insert(0, u'')     # create line break after "Arguments:"
            arg_string = u'\n'.join(arg_lines)
        else:
            arg_string = u' None'

        print output.format(command, description, arg_string)
    else:
        for name, (_, description) in commands.COMMANDS.iteritems():
            print u'{}:\t{}'.format(name, description)
    return True