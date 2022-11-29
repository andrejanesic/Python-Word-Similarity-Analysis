import numpy as np


class WordWave:
    """
    Encapsulates the sound wave of a single word.
    """

    def __init__(self, name: str, framerate: int, values: np.ndarray):
        """
        Default constructor. Takes in the file name and a NumPy 1-D array as input.
        """
        self.name = name
        self.framerate = framerate
        self.values = values
