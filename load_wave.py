from sound_wave import SoundWave
import wave
import numpy as np


def load_wave(filename: str):
    """
    Reads the wave file from <filename>. Returns the file as a SoundWave.
    """

    # This would normally go into a try-except clause but IO errors are not important for this program.
    try:
        wav = wave.open(filename, "r")
    except FileNotFoundError:
        print(f"File does not exist: {filename}")
        return None

    vals = np.frombuffer(wav.readframes(-1), np.int16)

    # Average of two channels if stereo file.
    if wav.getnchannels() > 1:
        ch1 = vals[0::2]
        ch2 = vals[1::2]

        # TODO this might be an SPOF, because we're averaging the two channels with floor division.
        vals = (ch1 + ch2) // 2

    return SoundWave(name=filename, wave=wav, values=vals)
