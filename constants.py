from handlers import *

STR_INVALID_COMMAND = 'Invalid command: "%s"'
STR_INVALID_ARG = 'Invalid argument: "%s"'
STR_INVALID_ARG_VALUE = 'Invalid value %s supplied for arg %s'
STR_INVALID_ARG_VALUES_COUNT = 'Argument %s accepts exactly %s values'
STR_INVALID_ARG_REQUIRED = 'Required argument %s not defined'
STR_BYE = 'Bye'
COMMANDS = {
    'load': {
        'about': 'Loads an audio file from the given path.',
        'positional_args': [
            {
                'about': 'Path to the audio file to load.',
                'arg': 'path',
                'values': 1,
                'type': 'string',
            }
        ],
        'handler': handle_load
    },
    'record': {
        'about': 'Records an audio file from input.',
        'named_args': [
            {
                'about': 'Path to the new audio file.',
                'arg': 'path',
                'optional': True,
                'values': 1,
                'type': 'string',
            }
        ],
        'handler': handle_record
    },
    'help': {
        'about': 'Shows this help dialog.',
        'handler': handle_help,
    },
    'exit': {
        'about': 'Exits the program.',
        'handler': handle_exit,
    }
}
