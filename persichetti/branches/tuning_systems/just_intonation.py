from .base import TuningSystem

class JustIntonationZarlino(TuningSystem):
    def __init__(self, base_freq=261.63):
        self.base_freq = base_freq
        self.ratios = {
            0: 1/1,
            2: 9/8,
            4: 5/4,
            5: 4/3,
            7: 3/2,
            9: 5/3,
            11: 15/8,
        }

    def name(self):
        return "Just Intonation (Zarlino)"

    def pitch_frequency(self, pitch_class: int, octave: int = 4) -> float:
        ratio = self.ratios.get(pitch_class % 12, 1.0)
        return self.base_freq * ratio * (2 ** (octave - 4))