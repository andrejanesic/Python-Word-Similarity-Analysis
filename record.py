# Code based on the following StackOverflow answer:
# https://stackoverflow.com/a/6743593

from sys import byteorder
from array import array
from struct import pack
import pyaudio
import wave
from time import time
import pathlib

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
SILENCE_END = 500


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True,
                    frames_per_buffer=CHUNK_SIZE)

    r = array('h')

    try:
        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

    except KeyboardInterrupt:
        pass

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    return sample_width, r


def record_to_file(path: str = None) -> str:
    "Records from the microphone and outputs the resulting data to 'path'"
    print('Press CTRL+C to stop recording.')
    if path == None:
        path = f'out/rec-{round(time())}.wav'
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    print(f'File saved to {path}')
    return path


if __name__ == '__main__':
    record_to_file()
