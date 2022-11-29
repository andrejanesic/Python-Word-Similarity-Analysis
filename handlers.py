import constants
import record
import load_wave
from state import state
import sys


def handle_record(args: dict = None):
    """
    Handles the recording of a new audio file.
    """
    if args:
        if args.get('named_args'):
            if args['named_args'].get('path'):
                record.record_to_file(args.path)
                return
    print('here')
    record.record_to_file()


def handle_load(args: dict = None):
    """
    Handles the routine of loading a new sound wave.
    """
    sw = load_wave(args['positional_args']['path'])
    state.add_sound_wave(sw)
    return


def handle_help(args: dict = None):
    """
    Shows the help menu.
    """
    for k, v in constants.COMMANDS.items():
        lines = []
        full_pattern = f'{k}'
        for argtype in ['positional_args', 'named_args']:
            if v.get(argtype):
                for arg in v[argtype]:
                    values = ''
                    if arg['values'] and arg['type']:
                        t = arg['type'] if argtype == 'named_args' else arg['arg']
                        if arg['values'] == '*':
                            values = f'<{t}>*'
                        else:
                            for i in range(0, arg['values']):
                                values += f'<{t}>'
                    if values and argtype == 'named_args':
                        values = ' ' + values
                    name = '-' + arg['arg'] if argtype == 'named_args' else ''
                    desc = ''
                    if arg.get('about'):
                        desc = ' - ' + arg['about']
                    pattern = f'{name}{values}'
                    if arg.get('optional'):
                        pattern = f'[{pattern}]'
                    lines.append({'pat': pattern, 'desc': desc})
                    full_pattern += ' ' + pattern
        ab = v['about']
        full_pattern += f' - {ab}'
        print(full_pattern)
        for l in lines:
            pat = l['pat']
            desc = l['desc']
            print(f'\t{pat} - {desc}')


def handle_exit(args: dict = None):
    print(constants.STR_BYE)
    sys.exit(0)
