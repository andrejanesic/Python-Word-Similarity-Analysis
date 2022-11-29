from sound_wave import SoundWave
import numpy as np


def dft(sw: SoundWave, window_t: int, window_func: str):
    """
    Discrete Fourier transform. Window_t in ms.
    """

    window_dur = window_t / 1000
    window_func = window_func.lower()

    # Calculate number of samples
    N = int(sw.wave.getframerate() * window_dur)

    # TODO check if we should be cutting this at all
    y = sw.values

    if len(y) == 0:
        raise ValueError("sw.values cannot be empty")
    if window_func != "none":
        i = 0
        while (i < len(y) // N):
            if window_func == "hamming":
                y[i*N:(i+1)*N] = y[i*N:(i+1)*N] * np.hamming(N)
            elif window_func == "hanning":
                y[i*N:(i+1)*N] = y[i*N:(i+1)*N] * np.hanning(N)
            else:
                return None
            i += 1

    # Slash right side and normalize
    y_temp = np.fft.fft(y)[0:int(N / 2)] / N
    y_temp[1:] = 2*y_temp[1:]

    # Calculate magnitude, remove complex part
    FFT_y = np.abs(y_temp)
    return FFT_y
