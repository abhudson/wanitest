#!/usr/bin/python
import util
import commands


if __name__ == '__main__':
    arg_parser = util.get_argument_parser()
    args = arg_parser.parse_args()

    try:
        commands.COMMANDS[args.command][0](*args.arguments)
    except TypeError as e:
        # Actually want to print help for this module
        if u'execute() takes' in e.message:
            arg_parser.print_help()
        else:
            raise
