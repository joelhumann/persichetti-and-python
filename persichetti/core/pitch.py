# pitch.py

DEFAULT_SPELLINGS = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
}

class PitchClass:
    def __init__(self, value):
        self.value = value % 12

    @property
    def name(self):
        return DEFAULT_SPELLINGS[self.value]

    def distance_to(self, other):
        return (other.value - self.value) % 12

    def __repr__(self):
        return f"PitchClass({self.value}) = {self.name}"


class Pitch:
    def __init__(self, index, reference_freq=440.0):
        self.index = index
        self.reference = reference_freq
        self.pc = PitchClass(index % 12)

    def frequency(self):
        return self.reference * (2 ** (self.index / 12))

    def __repr__(self):
        return f"Pitch({self.index}) = {self.pc.name}, {self.frequency():.2f} Hz"


