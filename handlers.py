import constants
import record
from load_wave import load_wave
from plot_waves import plot_sound_waves
from plot_waves import plot_word_waves
from database import database
import sys
import numpy as np
import matplotlib.pyplot as plt


def handle_list(args: dict = None):
    show_ww = True
    show_sw = True
    if args and args.get('named_args'):
        if args['named_args'].get('s'):
            show_ww = False
            show_sw = True
        if args['named_args'].get('w'):
            show_ww = True
            show_sw = False

    if show_ww:
        print("Loaded word waves:")
        if len(database.get_word_waves()) == 0:
            print("\tNo words waves loaded yet")
        for ww in database.get_word_waves():
            dur = round((ww.values.shape[0] * 1.0) / ww.framerate, 2)
            print(f"\t[W] {ww.name} - {dur}s")

    if show_sw:
        print("Loaded sound waves:")
        if len(database.get_sound_waves()) == 0:
            print("\tNo sound waves loaded yet")
        for sw in database.get_sound_waves():
            dur = round((sw.values.shape[0] * 1.0) / sw.wave.getframerate(), 2)
            cut = 'Processed' if sw.extracted else 'Not processed'
            print(f"\t[S] {sw.name} - {dur}s - {cut}")


def handle_record(args: dict = None):
    """
    Handles the recording of a new audio file.
    """
    p = None
    if args:
        if args.get('named_args'):
            if args['named_args'].get('path'):
                p = record.record_to_file(args.path)
    if p == None:
        p = record.record_to_file()
    sw = load_wave(p)
    database.add_sound_wave(sw)


def handle_load(args: dict = None):
    """
    Handles the routine of loading a new sound wave.
    """
    sw = load_wave(args['positional_args']['path'][0])
    database.add_sound_wave(sw)


def handle_plot(args: dict = None):
    """
    Handles the routine of plotting a sound wave.
    """
    sws = []
    wws = []

    if args and args.get('named_args') and args['named_args'].get('sounds'):
        names = args['named_args']['sounds']
        if names[0] == '*':
            sws = database.get_sound_waves()
        else:
            for n in names:
                f = False
                for sw in database.get_sound_waves():
                    if sw.name == n:
                        f = True
                        sws.append(sw)
                        break
                if not f:
                    print(constants.STR_ERR_SW_NOT_LOADED % n)
                    return

    if args and args.get('named_args') and args['named_args'].get('words'):
        names = args['named_args']['words']
        if names[0] == '*':
            wws = database.get_word_waves()
        else:
            for n in names:
                f = False
                for ww in database.get_word_waves():
                    if ww.name == n:
                        f = True
                        wws.append(ww)
                        break
                if not f:
                    print(constants.STR_ERR_WW_NOT_LOADED % n)
                    return

    if sws:
        plot_sound_waves(sws)
    if wws:
        plot_word_waves(wws)


def handle_extract(args: dict = None):
    """
    Extracts words from the given audio file.
    """
    sws = []
    if args and args.get('positional_args') and args['positional_args'].get('name'):
        names = args['positional_args']['name']
        for n in names:
            f = False
            for sw in database.get_sound_waves():
                if sw.name == n:
                    f = True
                    sws.append(sw)
                    break
            if not f:
                print(constants.STR_ERR_SW_NOT_LOADED % n)
                return
    else:
        sws = database.get_sound_waves()
    for sw in sws:
        extracted = sw.extract_words()
        if extracted:
            for ww in extracted:
                database.add_word_wave(ww)


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
                    if arg.get('values') and arg.get('type'):
                        t = arg['type'] if argtype == 'named_args' else arg['arg']
                        if arg['values'] == '*':
                            values = f'<{t}>*'
                        else:
                            for i in range(0, arg['values']):
                                if values != '':
                                    values += f' <{t}>'
                                else:
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


def handle_word(args: dict = None):
    """
    Handles management of WordWave objects.
    """

    if not args:
        return

    if (not args.get('positional_args')) or \
        (not args.get('named_args')) or \
            (not args['positional_args'].get('name')):
        return

    ww = database.get_sound_wave(args['positional_args']['name'][0])
    if not ww:
        print(constants.STR_ERR_WW_NOT_LOADED %
              args['positional_args']['name'])
        return

    for arg, vals in args['named_args'].items():

        if arg == 'rename':
            ww.name = vals[0]
            print(constants.STR_WW_RENAMED % ww.name)
            continue

        if arg == 'save':
            if vals[1] == 'raw':
                ww.save()
            elif vals[1] == 'lpc':
                ww.save('lpcs')
            elif vals[1] == 'mfcc':
                # TODO
                # ww.save('mfcc')
                pass
            else:
                # TODO
                pass
            continue


def handle_lpc(args: dict = None):
    """
    Handles the calculation of LPC for the selected word wave.
    """

    if not args:
        return

    if (not args.get('positional_args')) or \
            (not args['positional_args'].get('name')):
        return

    ww = database.get_sound_wave(args['positional_args']['name'][0])
    if not ww:
        print(constants.STR_ERR_WW_NOT_LOADED %
              args['positional_args']['name'])
        return

    window_l = 256
    shift = 128
    p = 32
    window_f = 'hamming'
    if args.get('named_args'):
        if args['named_args'].get('f'):
            window_f = args['named_args']['f'][0]
        if args['named_args'].get('w'):
            window_l = args['named_args']['w'][0]
        if args['named_args'].get('s'):
            shift = args['named_args']['s'][0]
        if args['named_args'].get('u'):
            if args['named_args']['u'][0] == 'samp':
                pass
            else:
                window_l = int(window_l * ww.framerate / 1000)
                shift = int(shift * ww.framerate / 1000)
        if args['named_args'].get('p'):
            p = args['named_args']['p'][0]

    lpc, err = ww.predict_lpc(window_l, shift, p, window_f)

    plt.ylabel("Amplitude")
    plt.xlabel("Time [s]")

    title = f"{ww.name} and LPC"
    time = np.linspace(0, len(ww.values) /
                       ww.framerate, num=len(ww.values))
    min_len = min(len(ww.values), len(lpc))
    plt.plot(time, ww.values[:min_len], label=f"{ww.name}")
    plt.plot(time, lpc[:min_len], '--', label=f"LPC")

    plt.title(title)
    plt.legend()
    plt.show()
    return


def handle_mfcc(args: dict = None):
    """
    Handles the calculation of MFCC for the selected word wave.
    """

    if not args:
        return

    if (not args.get('positional_args')) or \
            (not args['positional_args'].get('name')):
        return

    ww = database.get_sound_wave(args['positional_args']['name'][0])
    if not ww:
        print(constants.STR_ERR_WW_NOT_LOADED %
              args['positional_args']['name'])
        return

    window_l = 256
    window_f = 'hamming'
    filters_n = 10
    delta_t = 2
    if args.get('named_args'):
        if args['named_args'].get('f'):
            window_f = args['named_args']['f'][0]
        if args['named_args'].get('w'):
            window_l = args['named_args']['w'][0]
        if args['named_args'].get('m'):
            filters_n = args['named_args']['m'][0]
        if args['named_args'].get('t'):
            delta_t = args['named_args']['t'][0]
        if args['named_args'].get('u'):
            if args['named_args']['u'][0] == 'samp':
                pass
            else:
                window_l = int(window_l * ww.framerate / 1000)
        if args['named_args'].get('p'):
            p = args['named_args']['p'][0]

    cepstral_coefficients = ww.calc_mfcc(
        window_f, window_l, filters_n, delta_t)

    plt.figure(figsize=(15, 5))
    plt.plot(np.linspace(0, len(ww.values) /
                         ww.framerate, num=len(ww.values)), ww.values)
    plt.imshow(cepstral_coefficients, aspect='auto', origin='lower')
    plt.show()
    return
