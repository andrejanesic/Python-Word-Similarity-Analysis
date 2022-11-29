import lpc
import mfcc
from calc_dtw import calc_dtw
import numpy as np
import pathlib
import wave
import scipy.fftpack as fft
from scipy.signal import get_window
import matplotlib.pyplot as plt


class WordWave:
    """
    Encapsulates the sound wave of a single word.
    """

    def __init__(self, name: str, framerate: int, sample_width: int, values: np.ndarray):
        """
        Default constructor. Takes in the file name and a NumPy 1-D array as input.
        """
        self.name = name
        self.framerate = framerate
        self.sample_width = sample_width
        self.values = values
        self.lpc_prediction = None
        self.lpc_error = None
        self.mfcc = None

    def predict_lpc(self, window_l: int, shift: int, p: int, window_f: str = None):
        """
        Generates an LPC prediction of the signal. window_l must be specified in samples.
        """

        window = None
        if window_f == 'hamming':
            window = np.hamming(window_l)
        elif window_f == 'hanning':
            window = np.hanning(window_l)
        else:
            window = np.ones(window_l)

        overlap = shift / window_l
        self.lpc_prediction, self.lpc_error = lpc.prediction(
            self.values, window, p, overlap)
        return (self.lpc_prediction, self.lpc_error)

    def calc_mfcc(self, window_f: str, window_l: int, filters_n: int, t: int):
        """
        Calculates MFCC for word wave.
        """
        audio = mfcc.normalize_audio(self.values)

        hop_size = 15  # ms
        FFT_size = window_l

        audio_framed = mfcc.frame_audio(audio, FFT_size=FFT_size,
                                        hop_size=hop_size, sample_rate=self.framerate)

        if window_f == "hamming":
            window_f = "hamm"
        else:
            window_f = "hann"
        window = get_window(window_f, FFT_size, fftbins=True)
        audio_win = audio_framed * window

        audio_winT = np.transpose(audio_win)

        audio_fft = np.empty(
            (int(1 + FFT_size // 2), audio_winT.shape[1]), dtype=np.complex64, order='F')

        for n in range(audio_fft.shape[1]):
            audio_fft[:, n] = fft.fft(audio_winT[:, n], axis=0)[
                :audio_fft.shape[0]]

        audio_fft = np.transpose(audio_fft)
        audio_power = np.square(np.abs(audio_fft))

        freq_min = 0
        freq_high = self.framerate / 2
        mel_filter_num = filters_n

        filter_points, mel_freqs = mfcc.get_filter_points(
            freq_min, freq_high, mel_filter_num, FFT_size, sample_rate=44100)

        filters = mfcc.get_filters(filter_points, FFT_size)

        enorm = 2.0 / (mel_freqs[2:mel_filter_num+2] -
                       mel_freqs[:mel_filter_num])
        filters *= enorm[:, np.newaxis]

        audio_filtered = np.dot(filters, np.transpose(audio_power))
        audio_log = 10.0 * np.log10(audio_filtered)

        dct_filter_num = 40
        dct_filters = mfcc.dct(dct_filter_num, mel_filter_num)

        cepstral_coefficients = np.dot(dct_filters, audio_log)
        coeff_delta = mfcc.get_delta_values(cepstral_coefficients, t)
        coeff_delta_delta = mfcc.get_delta_values(coeff_delta, t)
        # np.vstack((cepstral_coefficients, coeff_delta, coeff_delta_delta))
        self.mfcc = cepstral_coefficients
        return self.mfcc

    def calc_dtw(self, template):
        """
        Calculates distance from template WordWave with DTW.
        """
        calc_dtw(self, template)

    def save(self, presentation: str = None):
        """
        Writes the word wave to ./out dir as a wav file.
        """

        fpath = './out/' + \
            (self.name if self.name.endswith('.wav') else self.name + '.wav')
        pathlib.Path(fpath).parent.mkdir(parents=True, exist_ok=True)
        wav = wave.open(fpath, "wb")
        wav.setframerate(self.framerate)
        wav.setnchannels(1)
        wav.setsampwidth(self.sample_width)
        wav.setnframes(len(self.values))

        # Write sound
        if presentation == None:
            wav.writeframes(self.values.astype(np.int16).tobytes())
        elif presentation == 'lpc':
            lpc = self.lpc_prediction
            if lpc == None:
                lpc, _ = self.predict_lpc(256, 64, 32, 'hamming')
            wav.writeframes(lpc.astype(np.int16).tobytes())
        elif presentation == 'mfcc':
            # TODO
            pass
        else:
            # TODO err?
            pass
        wav.close()
