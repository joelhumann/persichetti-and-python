# persichetti/fundamentals/pitch.py

DEFAULT_SPELLINGS = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
}


class PitchClass:
    """
    Represents a pitch class (modulo 12), using default spellings.
    """
    def __init__(self, value: int):
        self.value = value % 12

    @property
    def name(self) -> str:
        return DEFAULT_SPELLINGS[self.value]

    def distance_to(self, other: "PitchClass") -> int:
        return (other.value - self.value) % 12

    def __repr__(self) -> str:
        return f"PitchClass({self.value}) = {self.name}"


class Pitch:
    """
    Represents a pitch as a semitone index relative to a reference frequency.
    Index 69 corresponds to A440 by default (like MIDI).
    """
    def __init__(self, index: int, reference_freq: float = 440.0, reference_index: int = 69):
        self.index = index
        self.reference = reference_freq
        self.reference_index = reference_index
        self.pc = PitchClass(index)

    def frequency(self) -> float:
        return self.reference * (2 ** ((self.index - self.reference_index) / 12))

    def distance_to(self, other: "Pitch") -> int:
        return other.index - self.index

    def __repr__(self) -> str:
        return f"Pitch({self.index}) = {self.pc.name}, {self.frequency():.2f} Hz"
