from typing import Optional, Set
from sound_wave import SoundWave
from word_wave import WordWave


class Database:
    """
    Global application state.
    """

    def __init__(self):
        self.__sound_waves = set()
        self.__word_waves = set()

    def add_sound_wave(self, sw: SoundWave):
        self.__sound_waves.add(sw)

    def remove_sound_wave(self, sw: SoundWave):
        if not (sw in self.__sound_waves):
            return
        self.__sound_waves.remove(sw)

    def get_sound_waves(self) -> Set[SoundWave]:
        return self.__sound_waves

    def get_sound_wave(self, name: str) -> Optional[SoundWave]:
        t = None
        for sw in self.__sound_waves:
            if sw.name == name:
                t = sw
                break
        return t

    def add_word_wave(self, ww: WordWave):
        self.__word_waves.add(ww)

    def remove_word_wave(self, ww: WordWave):
        if not (ww in self.__word_waves):
            return
        self.__word_waves.remove(ww)

    def get_word_waves(self) -> Set[WordWave]:
        return self.__word_waves

    def get_sound_wave(self, name: str) -> Optional[WordWave]:
        t = None
        for ww in self.__word_waves:
            if ww.name == name:
                t = ww
                break
        return t


database = Database()
