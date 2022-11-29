from sound_wave import SoundWave
from word_wave import WordWave
from dft import dft
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def plot_sound_waves(
        sound_waves: List[SoundWave],
        plot_type="waveform",
        window_t=None,
        window_func: str = "none"):
    """
    Plots all passed sound waves on a single plot with the given type.
    """
    title = f"{plot_type.capitalize()} plot of"

    if plot_type == "waveform":

        plt.ylabel("Amplitude")
        plt.xlabel("Time [s]")

        for sw in sound_waves:
            axv_labelled = False
            title += f" {sw.name}.wav"
            _, noise_borders = sw.find_endpoints(500, 5000)
            time = np.linspace(0, len(sw.values) /
                               sw.wave.getframerate(), num=len(sw.values))
            # TODO check if okay to simply plot different times
            plt.plot(time, sw.values, label=f"{sw.name}.wav")
            clr = np.random.rand(3,)
            if not sw.extracted:
                for xc in noise_borders:
                    if axv_labelled:
                        plt.axvline(x=xc, color=clr)
                    else:
                        plt.axvline(x=xc, color=clr,
                                    label=f"{sw.name} speech border")
                        axv_labelled = True

        plt.title(title)
        plt.legend()
        plt.show()
        return

    if plot_type == "histogram":

        plt.ylabel("Magnitude")
        plt.xlabel("Frequency [Hz]")
        plt.xscale('log')
        plt.yscale('log')

        if window_t == None:
            window_t = 100
        window_dur = window_t / 1000

        for sw in sound_waves:

            title += f" {sw.name}.wav"
            N = int(sw.wave.getframerate() * window_dur)
            f = sw.wave.getframerate() * np.arange(N / 2) / N
            # TODO check if okay to simply plot different freqs
            y = dft(sw, window_t=window_t, window_func=window_func)
            y = y + y.min()
            y = y / y.max() * 100
            # plt.plot(f, y, label=f"{sw.name}.wav")
            # TODO fix
            plt.bar(f, y, align="center", width=f[1]-f[0])

        title += f", window_t={window_t}, window_func={window_func}"
        plt.title(title)
        plt.legend()
        plt.show()
        return

    if plot_type == "spectrogram":

        if len(sound_waves) > 1:
            raise ValueError("Spectrogram can only plot 1 sound wave")

        sw = sound_waves[0]
        M = 1024

        if window_func == "none" or window_func == None:
            freqs, times, Sx = signal.spectrogram(
                sw.values,
                fs=sw.wave.getframerate(),
                nperseg=M,
                noverlap=M - window_t,
                detrend=False, scaling='spectrum'
            )
        elif window_func in ["hamming", "hanning"]:
            freqs, times, Sx = signal.spectrogram(
                sw.values,
                fs=sw.wave.getframerate(),
                window=window_func,
                nperseg=M,
                noverlap=M - window_t,
                detrend=False, scaling='spectrum'
            )
        else:
            raise ValueError(
                "window_func argument can only be one of [None, \"hamming\", \"hanning\"]")

        mesh = plt.pcolormesh(times, freqs / 1000, 10 *
                              np.log10(Sx), cmap='viridis')
        plt.colorbar(mappable=mesh)
        plt.ylabel('Frequency [kHz]')
        plt.xlabel('Time [s]')
        plt.grid(axis='y')
        plt.title(
            f"Spectrogram plot of {sw.name}.wav, window_t={window_t}, window_func={window_func}")

        axv_labelled = False
        _, noise_borders = sw.find_endpoints(500, 5000)
        clr = np.random.rand(3,)
        if not sw.extracted:
            for xc in noise_borders:
                if axv_labelled:
                    plt.axvline(x=xc, color=clr)
                else:
                    plt.axvline(x=xc, color=clr,
                                label=f"{sw.name} speech border")
                    axv_labelled = True

        plt.legend()
        plt.show()
        return

    raise ValueError(
        "Invalid plot_type passed to function plot_waves: " + plot_type)


def plot_word_waves(
        word_waves: List[WordWave],
        plot_type="waveform",
        window_t=None,
        window_func: str = "none"):
    """
    Plots all passed word waves on a single plot with the given type.
    """
    title = f"{plot_type.capitalize()} plot of"

    if plot_type == "waveform":

        plt.ylabel("Amplitude")
        plt.xlabel("Time [s]")

        for ww in word_waves:
            title += f" {ww.name}"
            time = np.linspace(0, len(ww.values) /
                               ww.framerate, num=len(ww.values))
            plt.plot(time, ww.values, label=f"{ww.name}")

        plt.title(title)
        plt.legend()
        plt.show()
        return

    if plot_type == "histogram":

        plt.ylabel("Magnitude")
        plt.xlabel("Frequency [Hz]")
        plt.xscale('log')
        plt.yscale('log')

        if window_t == None:
            window_t = 100
        window_dur = window_t / 1000

        for ww in word_waves:

            title += f" {ww.name}.wav"
            N = int(ww.framerate * window_dur)
            f = ww.framerate * np.arange(N / 2) / N
            # TODO check if okay to simply plot different freqs
            y = dft(ww, window_t=window_t, window_func=window_func)
            y = y + y.min()
            y = y / y.max() * 100
            # plt.plot(f, y, label=f"{ww.name}.wav")
            # TODO fix
            plt.bar(f, y, align="center", width=f[1]-f[0])

        title += f", window_t={window_t}, window_func={window_func}"
        plt.title(title)
        plt.legend()
        plt.show()
        return

    if plot_type == "spectrogram":

        if len(word_waves) > 1:
            raise ValueError("Spectrogram can only plot 1 word wave")

        ww = word_waves[0]
        M = 1024

        if window_func == "none" or window_func == None:
            freqs, times, Sx = signal.spectrogram(
                ww.values,
                fs=ww.framerate,
                nperseg=M,
                noverlap=M - window_t,
                detrend=False, scaling='spectrum'
            )
        elif window_func in ["hamming", "hanning"]:
            freqs, times, Sx = signal.spectrogram(
                ww.values,
                fs=ww.framerate,
                window=window_func,
                nperseg=M,
                noverlap=M - window_t,
                detrend=False, scaling='spectrum'
            )
        else:
            raise ValueError(
                "window_func argument can only be one of [None, \"hamming\", \"hanning\"]")

        mesh = plt.pcolormesh(times, freqs / 1000, 10 *
                              np.log10(Sx), cmap='viridis')
        plt.colorbar(mappable=mesh)
        plt.ylabel('Frequency [kHz]')
        plt.xlabel('Time [s]')
        plt.grid(axis='y')
        plt.title(
            f"Spectrogram plot of {ww.name}.wav, window_t={window_t}, window_func={window_func}")

        plt.legend()
        plt.show()
        return

    raise ValueError(
        "Invalid plot_type passed to function plot_waves: " + plot_type)
