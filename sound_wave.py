from typing import List
import wave
import numpy as np
import constants
from word_wave import WordWave
from time import time


class SoundWave:
    """
    Encapsulates the wave file and its associated operations.
    """

    def __init__(self, name: str, wave: wave.Wave_read, values: np.ndarray):
        """
        Default constructor. Takes in the file name and a NumPy 1-D array as input.
        """
        self.name = name
        self.wave = wave
        self.values = values
        self.words = []
        self.extracted = False
        self.speech_detected = False

    def find_endpoints(self, p: int = 0, r: int = 0):
        """
        Finds the endpoints of speech on the sound wave. Returns noise mask and borders.
        """
        if p == 0:
            p = constants.PARAM_EXTRACT_P
        if r == 0:
            r = constants.PARAM_EXTRACT_R

        # Get the number of frames for the first 100ms.
        initial_t = 100
        initial_t = round((self.wave.getframerate()) * initial_t / 1000)
        initial_f = np.absolute(self.values[:initial_t])

        # Noise limit.
        noise_l = np.average(initial_f) + 2 * initial_f.std()
        noise_mask = np.zeros(self.values.shape)

        # Window width (ms) for noise detection.
        window_w = 10
        window_w = round(self.wave.getframerate() * window_w / 100)

        i = 0
        while i < len(self.values):
            # TODO pitati jel treba i ovde abs
            window_avg = np.average(np.absolute(self.values[i:(i+window_w)]))
            j = 1 if window_avg > noise_l else 0
            noise_mask[i:(i+window_w)] = j
            i += window_w

        length = 0
        start = -1
        curr = 0
        while curr < len(noise_mask):
            if noise_mask[curr] == 1:
                if length < p:
                    noise_mask[start+1:start+1+length] = 1
                start = curr
                length = 0
            curr += 1
            length += 1

        length = 0
        start = -1
        curr = 0
        while curr < len(noise_mask):
            if noise_mask[curr] == 0:
                if length < r:
                    noise_mask[start+1:start+1+length] = 0
                start = curr
                length = 0
            curr += 1
            length += 1

        # Find borders of noise.
        shift_l = noise_mask.tolist().copy()
        shift_l.pop(0)
        shift_l.append(0)
        shift_r = noise_mask.tolist().copy()
        shift_r.pop()
        shift_r.insert(0, 0)
        noise_borders = ((noise_mask - np.array(shift_l) >
                          0) | (noise_mask - np.array(shift_r) > 0)).astype(int)
        noise_borders = (np.array(np.nonzero(noise_borders)) /
                         self.wave.getframerate())[0].tolist()

        return (noise_mask, noise_borders)

    def extract_words(self, p: int = 0, r: int = 0) -> List[WordWave]:
        """
        Extracts a list of WordWaves detected in the SoundWave.
        """

        if self.extracted:
            return self.words
        noise_mask, noise_borders = self.find_endpoints(p, r)

        self.speech_detected = noise_mask.sum() > 0
        if self.speech_detected == False:
            self.extracted = True
            print(constants.STR_ERR_NO_WORDS_FOUND % self.name)
            return

        if len(noise_borders) % 2 == 1:
            print(constants.STR_ERR_ODD_WORD_INDICES_COUNT %
                  len(noise_borders))
            return

        words_raw = []
        values_cleaned = np.multiply(self.values, noise_mask)
        for i in range(0, len(noise_borders) // 2):
            ind_l = int(noise_borders[i] * self.wave.getframerate())
            ind_r = int(noise_borders[i + 1] * self.wave.getframerate() + 1)
            words_raw.append(values_cleaned[ind_l:ind_r])

        self.words = []
        for i in range(0, len(words_raw)):
            ww = WordWave(f'word-{int(time())}-{i}',
                          self.wave.getframerate(), words_raw[i])
            self.words.append(ww)
        self.extracted = True
        print(f"Extracted {len(self.words)} words from sound wave {self.name}")
        return self.words
