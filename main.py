import constants
from record import record_to_file
import sys


def main():
    try:
        while True:

            # Get input and check if valid initial command
            cmd = input('> ')
            cmd = cmd.split()
            if len(cmd) < 1:
                continue
            if not (cmd[0] in constants.COMMANDS.keys()):
                print(constants.STR_INVALID_COMMAND % cmd[0])
                continue

            # Check all args
            cmdset = constants.COMMANDS[cmd[0]]
            args = {
                'positional_args': {},
                'named_args': {},
            }
            exec_comm = True
            for arg_type in ['positional_args', 'named_args']:
                if cmdset.get(arg_type):
                    valid_all = True
                    for arg in cmdset[arg_type]:
                        err = None
                        found = False
                        vals = None
                        for user_arg in cmd[0:]:
                            if (arg_type == 'positional_args') or (arg_type == 'named_args' and (user_arg.lower() == '-' + arg['arg'])):
                                ind = cmd.index(user_arg)
                                found = True
                                vals = []
                                if arg.get('values') and arg.get('type'):
                                    if arg['values'] != 0:
                                        for i in range(ind + 1, len(cmd)):
                                            argv = cmd[i]
                                            if argv.startswith('-'):
                                                break
                                            t = argv
                                            try:
                                                if arg['type'] == 'string':
                                                    pass
                                                elif arg['type'] == 'int':
                                                    t = int(argv)
                                                elif arg['type'] == 'float':
                                                    t = float(argv)
                                                elif arg['type'] == 'boolean':
                                                    t = argv == 'true'
                                                elif len(arg['type'].split('|')) > 0:
                                                    possible_values = arg['type'] \
                                                        .split('|')
                                                    if t not in possible_values:
                                                        raise ValueError
                                                else:
                                                    n = arg['arg']
                                                    raise ValueError(
                                                        f'Invalid arg type defined for {cmd[0]}.args.{n}'
                                                    )
                                            except ValueError:
                                                if type(arg['arg']) == type([]):
                                                    err = constants.STR_INVALID_ARG_VALUE % (argv, arg['arg'][0])
                                                else:
                                                    err = constants.STR_INVALID_ARG_VALUE % (argv, arg['arg'])
                                                break
                                            vals.append(t)

                                    if arg['values'] == '*':
                                        pass
                                    elif arg['values'] == 0:
                                        pass
                                    else:
                                        if len(vals) != arg['values']:
                                            err = constants.STR_INVALID_ARG_VALUES_COUNT % (arg[
                                                'arg'], arg['values'])
                                            break
                                        pass
                                break

                        if not found:
                            if arg.get('optional'):
                                continue
                            else:
                                err = constants.STR_INVALID_ARG_REQUIRED % arg['arg']

                        if err:
                            print(err)
                            constants.COMMANDS['help']['handler']({})
                            valid_all = False
                            break

                        args[arg_type][arg['arg']] = vals

                    # If all valid, proceed with exec
                    if not valid_all:
                        exec_comm = False
                        break

            # Call handler
            if exec_comm:
                cmdset['handler'](args)
    except KeyboardInterrupt:
        constants.COMMANDS['exit']['handler']({})


if __name__ == '__main__':
    main()
