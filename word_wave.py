import lpc
import numpy as np
import pathlib
import wave


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
