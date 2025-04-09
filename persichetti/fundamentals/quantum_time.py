# persichetti/fundamentals/quantum_time.py

from decimal import Decimal
from fractions import Fraction
from functools import reduce
from math import lcm
from typing import Union, Callable


class ClockTime:
    """
    Represents an absolute point in physical (Clock) time.

    .. :noindex:
    """

    def __init__(self, seconds):
        self.seconds = Decimal(seconds)

    @property
    def seconds(self) -> Decimal:
        """Duration in seconds."""
        return self._seconds

    def __sub__(self, other):
        return ClockDuration(self.seconds - other.seconds)

    def __add__(self, duration):
        return ClockTime(self.seconds + duration.seconds)

    def __repr__(self):
        return f"ClockTime({self.seconds} s)"


class ClockDuration:
    """
    Represents a duration or interval between two points in ClockTime.

    .. :noindex:
    """

    def __init__(self, seconds):
        self.seconds = Decimal(seconds)

    @property
    def seconds(self) -> Decimal:
        """Duration in seconds."""
        return self._seconds

    def __add__(self, other):
        return ClockDuration(self.seconds + other.seconds)

    def __repr__(self):
        return f"ClockDuration(\u0394{self.seconds} s)"


class TempoFunction:
    """
    Represents a constant tempo function for a Musical Inertial Frame.

    .. :noindex:
    """

    def __init__(self, bpm=60):
        self.bpm = Decimal(bpm)
        self.seconds_per_beat = Decimal(60) / self.bpm

    @property
    def bpm(self) -> Decimal:
        """Beats per minute."""
        return self._bpm

    def beats_to_seconds(self, beats):
        return ClockDuration(beats * self.seconds_per_beat)

    def seconds_to_beats(self, seconds):
        return Decimal(seconds) / self.seconds_per_beat
    
    @property
    def seconds_per_beat(self) -> Decimal:
        """Duration of one beat in seconds."""
        return self._seconds_per_beat

    def __repr__(self):
        return f"TempoFunction({self.bpm} BPM)"


class MusicalInertialFrame:
    def __init__(self, tempo_function: TempoFunction, start_time: ClockTime):
        self.tempo_function = tempo_function
        self.start_time = start_time
    """
    Defines a local temporal reference frame for a musical voice.

    .. :noindex:
    """

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

    .. :noindex:
    """

    def __init__(self):
        self.frames = []

    @property
    def frames(self) -> list:
        """Resolved temporal frames in the timeline."""
        return self._frames

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
    def __init__(self, fqmt: Fraction, seconds_per_fqmt: Union[Decimal, Callable[[int], Decimal]]):
        self.fqmt = fqmt
        self.seconds_per_fqmt = seconds_per_fqmt

    @property
    def fqmt(self) -> Fraction:
        """Fundamental Quantum of Musical Time (FQMT)."""
        return self._fqmt
    
    """
    Maps the Fundamental Quantum of Musical Time (FQMT) to real ClockTime.

    .. :noindex:
    """

    def musical_to_clock(self, tick_index: int) -> ClockTime:
        if callable(self.seconds_per_fqmt):
            seconds = sum(self.seconds_per_fqmt(i) for i in range(tick_index))
        else:
            seconds = tick_index * self.seconds_per_fqmt
        return ClockTime(seconds)

    def set_tempo(self, bpm_for_unit: Fraction):
        seconds = Decimal(60) / Decimal(bpm_for_unit)
        self.seconds_per_fqmt = seconds

    @property
    def seconds_per_fqmt(self) -> Union[Decimal, Callable[[int], Decimal]]:
        """Duration of one FQMT unit in seconds."""
        return self._seconds_per_fqmt

class TimeContext:
    """
    A container for local temporal information governing motif resolution,
    including the base rhythmic unit (quantum of time) and other optional
    timing parameters.
    """
           
    def __init__(self, base_note=None, **kwargs):
        # Safely initialize base_note if provided
        self._base_note = base_note
        # Initialize other optional arguments if needed
        # (e.g., self.quantum_unit, self.time_signature, etc.)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def base_note(self):
        """The rhythmic base unit used as the quantum of time."""
        return self._base_note

    @base_note.setter
    def base_note(self, value):
        self._base_note = value  

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

