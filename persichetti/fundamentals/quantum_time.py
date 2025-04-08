# persichetti/fundamentals/quantum_time.py

from decimal import Decimal
from fractions import Fraction
from functools import reduce
from math import lcm
from typing import Union, Callable


class ClockTime:
    """
    Represents an absolute point in physical (Clock) time.

    Attributes:
        seconds (Decimal): The time value in seconds.
    """
    seconds: Decimal

    def __init__(self, seconds):
        self.seconds = Decimal(seconds)

    def __sub__(self, other):
        return ClockDuration(self.seconds - other.seconds)

    def __add__(self, duration):
        return ClockTime(self.seconds + duration.seconds)

    def __repr__(self):
        return f"ClockTime({self.seconds} s)"


class ClockDuration:
    """
    Represents a duration or interval between two points in ClockTime.

    Attributes:
        seconds (Decimal): Duration in seconds.
    """
    seconds: Decimal

    def __init__(self, seconds):
        self.seconds = Decimal(seconds)

    def __add__(self, other):
        return ClockDuration(self.seconds + other.seconds)

    def __repr__(self):
        return f"ClockDuration(\u0394{self.seconds} s)"


class TempoFunction:
    """
    Represents a constant tempo function for a Musical Inertial Frame.

    Attributes:
        bpm (Decimal): Beats per minute.
        seconds_per_beat (Decimal): Duration of one beat in seconds.
    """
    bpm: Decimal
    seconds_per_beat: Decimal

    def __init__(self, bpm=60):
        self.bpm = Decimal(bpm)
        self.seconds_per_beat = Decimal(60) / self.bpm

    def beats_to_seconds(self, beats):
        return ClockDuration(beats * self.seconds_per_beat)

    def seconds_to_beats(self, seconds):
        return Decimal(seconds) / self.seconds_per_beat

    def __repr__(self):
        return f"TempoFunction({self.bpm} BPM)"


class MusicalInertialFrame:
    """
    Defines a local temporal reference frame for a musical voice.

    Attributes:
        tempo_function (TempoFunction): Governs the beat-to-clock mapping.
        start_time (ClockTime): The starting time of the frame in ClockTime.
    """
    tempo_function: TempoFunction
    start_time: ClockTime

    def __init__(self, tempo_function: TempoFunction, start_time: ClockTime):
        self.tempo_function = tempo_function
        self.start_time = start_time

    def beat_to_clock_time(self, beat_number):
        offset = self.tempo_function.beats_to_seconds(beat_number)
        return self.start_time + offset

    def clock_time_to_beat(self, clock_time: ClockTime):
        delta = clock_time - self.start_time
        return self.tempo_function.seconds_to_beats(delta.seconds)

    def __repr__(self):
        return f"MIF(start={self.start_time}, tempo={self.tempo_function})"


class FQMTResolver:
    """
    Computes the Fundamental Quantum of Musical Time (FQMT) for a set of Musical Inertial Frames.

    Attributes:
        frames (list of Fraction): List of smallest unit durations (in seconds) per MIF.
    """
    frames: list

    def __init__(self):
        self.frames = []

    def add_frame(self, mif: MusicalInertialFrame, smallest_unit_in_beats: Fraction):
        duration_in_seconds = smallest_unit_in_beats * Decimal(mif.tempo_function.seconds_per_beat)
        self.frames.append(Fraction(duration_in_seconds))

    def compute_fqmt(self):
        if not self.frames:
            raise ValueError("No frames added to FQMTResolver.")
        denominators = [duration.limit_denominator().denominator for duration in self.frames]
        seconds_per_tick = Fraction(1, lcm(*denominators))
        return seconds_per_tick

    def __repr__(self):
        fq = self.compute_fqmt()
        return f"FQMT = {fq} seconds"


class TimeMapping:
    """
    Maps the Fundamental Quantum of Musical Time (FQMT) to real ClockTime.

    Attributes:
        fqmt (Fraction): The quantum unit in musical time.
        seconds_per_fqmt (Decimal or callable): Duration of one FQMT in seconds or a function.
    """
    fqmt: Fraction
    seconds_per_fqmt: Union[Decimal, Callable[[int], Decimal]]

    def __init__(self, fqmt: Fraction, seconds_per_fqmt):
        self.fqmt = fqmt
        self.seconds_per_fqmt = seconds_per_fqmt

    def musical_to_clock(self, tick_index: int) -> ClockTime:
        if callable(self.seconds_per_fqmt):
            seconds = sum(self.seconds_per_fqmt(i) for i in range(tick_index))
        else:
            seconds = tick_index * self.seconds_per_fqmt
        return ClockTime(seconds)

    def set_tempo(self, bpm_for_unit: Fraction):
        seconds = Decimal(60) / Decimal(bpm_for_unit)
        self.seconds_per_fqmt = seconds


class TimeContext:
    """
    Maps quantum durations (quanta) to LilyPond durations using a base note value.

    Attributes:
        base_note (int): The note value that represents one quantum (e.g., 64 = 1/64 note).
    """
    base_note: int

    def __init__(self, base_note: int = 64):
        if base_note not in [1, 2, 4, 8, 16, 32, 64, 128]:
            raise ValueError("Use a standard LilyPond duration as base_note (e.g., 4, 8, 16, 32, 64).")
        self.base_note = base_note

    def quanta_to_lilypond(self, quanta: int) -> str:
        duration = Fraction(quanta, 1) * Fraction(1, self.base_note)
        return self._fraction_to_lilypond(duration)

    def _fraction_to_lilypond(self, duration: Fraction) -> str:
        base = 1
        dots = 0
        while duration < Fraction(1, base):
            base *= 2

        value = Fraction(1, base)
        leftover = duration - value

        while leftover > 0:
            base *= 2
            dot_value = Fraction(1, base)
            leftover -= dot_value
            if leftover >= 0:
                dots += 1

        lily = str(base)
        if dots > 0:
            lily += "." * dots
        return lily

