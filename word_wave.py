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

    def save(self):
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
        wav.writeframes(self.values.astype(np.int16).tobytes())
        wav.close()
