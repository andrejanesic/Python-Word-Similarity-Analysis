from sound_wave import SoundWave


class State:
    """
    Global application state.
    """

    def __init__(self):
        self.__sound_waves = set()

    def add_sound_wave(self, sw: SoundWave):
        self.__sound_waves.add(sw)

    def remove_sound_wave(self, sw: SoundWave):
        if not (sw in self.__sound_waves):
            return
        self.__sound_waves.remove(sw)


state = State()
