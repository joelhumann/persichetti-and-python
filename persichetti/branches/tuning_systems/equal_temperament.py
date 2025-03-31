from .base import TuningSystem
import math

class EqualTemperament(TuningSystem):
    def __init__(self, base_freq=440.0, reference_note=("A", 4), divisions=12):
        self.base_freq = base_freq
        self.ref_pc = self.note_to_pc(reference_note[0])
        self.ref_octave = reference_note[1]
        self.divisions = divisions

    def name(self):
        return f"{self.divisions}-TET"

    def pitch_frequency(self, pitch_class: int, octave: int = 4) -> float:
        n = (octave - self.ref_octave) * self.divisions + (pitch_class - self.ref_pc)
        freq = self.base_freq * (2 ** (n / self.divisions))
        return round(freq, 2) # Round to 2 decimal places for display clarity

    @staticmethod
    def note_to_pc(name: str) -> int:
        spellings = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        return spellings.index(name.upper())