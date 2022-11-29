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
STR_WW_RENAMED = 'Word wave renamed to "%s"'
STR_ERR_BAD_LPC_OPERANDS = 'The passed LPC operands do not compute mathematically. Try overlap value of 0.5'
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
    'word': {
        'about': 'Central command for managing word waves.',
        'positional_args': [
            {
                'about': 'Name of the word to manage.',
                'arg': 'name',
                'values': 1,
                'type': 'string',
            },
        ],
        'named_args': [
            {
                'about': 'Renames the selected word wave to the new name.',
                'arg': 'rename',
                'optional': True,
                'values': 1,
                'type': 'string',
            },
            {
                'about': 'Saves the selected word into ./out with the given representation (appended to file name.)',
                'arg': 'save',
                'optional': True,
                'values': 1,
                'type': 'raw|lpc|mfcc',
            },
        ],
        'handler': handle_word,
    },
    'lpc': {
        'about': 'Calculates an LPC prediction for the given word wave.',
        'positional_args': [
            {
                'about': 'Name of the word wave to calculate LPC for.',
                'arg': 'name',
                'values': 1,
                'type': 'string',
            },
        ],
        'named_args': [
            {
                'about': 'Window function.',
                'arg': 'f',
                'optional': True,
                'values': 1,
                'type': 'hamming|hanning|none',
            },
            {
                'about': 'Window size/shift parameter unit (miliseconds or samples).',
                'arg': 'u',
                'optional': True,
                'values': 1,
                'type': 'ms|samp',
            },
            {
                'about': 'Window size, in pre-defined unit (defaults to # samples).',
                'arg': 'w',
                'optional': True,
                'values': 1,
                'type': 'int',
            },
            {
                'about': 'Window shift in pre-defined unit (defaults to # samples).',
                'arg': 's',
                'optional': True,
                'values': 1,
                'type': 'int',
            },
            {
                'about': 'Precision coefficient.',
                'arg': 'p',
                'optional': True,
                'values': 1,
                'type': 'int',
            },
        ],
        'handler': handle_lpc,
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
