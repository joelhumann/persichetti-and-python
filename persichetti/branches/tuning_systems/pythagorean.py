from .base import TuningSystem

class PythagoreanTuning(TuningSystem):
    def __init__(self, base_freq=261.63):
        self.base_freq = base_freq
        self.ratios = {
            0: 1.0,
            2: 9/8,
            4: 81/64,
            5: 4/3,
            7: 3/2,
            9: 27/16,
            11: 243/128
        }

    def name(self):
        return "Pythagorean Tuning"

    def pitch_frequency(self, pitch_class: int, octave: int = 4) -> float:
        ratio = self.ratios.get(pitch_class % 12, 1.0)
        return self.base_freq * ratio * (2 ** (octave - 4))