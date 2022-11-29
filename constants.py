from handlers import *

STR_INVALID_COMMAND = 'Invalid command: "%s"'
STR_INVALID_ARG = 'Invalid argument: "%s"'
STR_INVALID_ARG_VALUE = 'Invalid value %s supplied for arg %s'
STR_INVALID_ARG_VALUES_COUNT = 'Argument %s accepts exactly %s values'
STR_INVALID_ARG_REQUIRED = 'Required argument %s not defined'
STR_BYE = 'Bye'
STR_ERR_ODD_WORD_INDICES_COUNT = 'Detected odd number of word indices: %d'
STR_ERR_NO_WORDS_FOUND = 'No words found to extract in sound wave %s'
STR_ERR_SW_NOT_LOADED = 'Sound wave "%s" not loaded, did you forget to load it?'
STR_ERR_WW_NOT_LOADED = 'Word wave "%s" does not exist'
PARAM_EXTRACT_P = 2000
PARAM_EXTRACT_R = 7500
COMMANDS = {
    'list': {
        'about': 'Lists all loaded sound waves and words.',
        'named_args': [
            {
                'arg': 'w',
                'optional': True,
                'about': 'List only words. Takes precedence over -s argument.',
            },
            {
                'arg': 's',
                'optional': True,
                'about': 'List only sound waves.'
            }
        ],
        'handler': handle_list,
    },
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
    'plot': {
        'about': 'Plots the given sound or word wave(s)',
        'named_args': [
            {
                'about': 'Names of the extracted word waves to plot.',
                'arg': 'words',
                'values': '*',
                'optional': True,
                'type': 'string',
            },
            {
                'about': 'Names of the loaded sound waves to plot.',
                'arg': 'sounds',
                'values': '*',
                'optional': True,
                'type': 'string',
            }
        ],
        'handler': handle_plot,
    },
    'extract': {
        'about': 'Extracts words from the given sound wave(s).',
        'positional_args': [
            {
                'about': 'Name(s) of the loaded sound waves to extract words from.',
                'arg': 'name',
                'values': '*',
                'optional': True,
                'type': 'string',
            }
        ],
        'handler': handle_extract,
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
