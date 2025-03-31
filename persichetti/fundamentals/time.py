"""
quantum_time.py

Philosophical and computational model of musical time based on the Persichetti and Python Project.
Supports absolute clock time, local musical inertial frames, tempo functions, and computation of
the Fundamental Quantum of Musical Time (FQMT).
"""

from decimal import Decimal
from fractions import Fraction
from functools import reduce
from math import lcm


class ClockTime:
    """
    Represents an absolute point in physical (Clock) time.

    Attributes:
        seconds (Decimal): The time value in seconds.
    """
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

    Methods:
        beats_to_seconds(beats): Converts a number of beats to seconds.
        seconds_to_beats(seconds): Converts seconds to number of beats.
    """
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

    Methods:
        beat_to_clock_time(beat_number): Converts a beat number to ClockTime.
        clock_time_to_beat(clock_time): Converts a ClockTime to local beat number.
    """
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

    Methods:
        add_frame(mif, smallest_unit_in_beats): Adds a frame with its smallest pulse unit.
        compute_fqmt(): Computes the least common multiple of all unit durations.
    """
    def __init__(self):
        self.frames = []

    def add_frame(self, mif: MusicalInertialFrame, smallest_unit_in_beats: Fraction):
        """
        Adds a musical frame and its smallest unit (in beats).
        
        Args:
            mif (MusicalInertialFrame): The frame to include.
            smallest_unit_in_beats (Fraction): The smallest unit of meter in beats (e.g., 1/8).
        """
        duration_in_seconds = smallest_unit_in_beats * Decimal(mif.tempo_function.seconds_per_beat)
        self.frames.append(Fraction(duration_in_seconds))

    def compute_fqmt(self):
        """
        Computes the Fundamental Quantum of Musical Time (FQMT) in seconds as a Fraction.
        
        Returns:
            Fraction: The smallest quantum of time that resolves all metrical frames.
        """
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
        fqmt (Fraction): The quantum unit in musical time (e.g., 1/144 of a whole note).
        seconds_per_fqmt (Decimal or callable): Duration of one FQMT in seconds or a time-varying function.

    Methods:
        musical_to_clock(tick_index): Converts a tick index to absolute ClockTime.
        set_tempo(bpm_for_unit): Sets a fixed metronomic speed for the FQMT.
    """
    def __init__(self, fqmt: Fraction, seconds_per_fqmt):
        self.fqmt = fqmt
        self.seconds_per_fqmt = seconds_per_fqmt  # Can be Decimal or function

    def musical_to_clock(self, tick_index: int) -> ClockTime:
        """
        Maps a musical tick (multiple of FQMT) to absolute ClockTime.

        Args:
            tick_index (int): The index of the musical quantum.

        Returns:
            ClockTime: The mapped ClockTime.
        """
        if callable(self.seconds_per_fqmt):
            seconds = sum(self.seconds_per_fqmt(i) for i in range(tick_index))
        else:
            seconds = tick_index * self.seconds_per_fqmt
        return ClockTime(seconds)

    def set_tempo(self, bpm_for_unit: Fraction):
        """
        Set the duration of each FQMT unit based on a desired tempo.

        Args:
            bpm_for_unit (Fraction): The number of FQMTs per minute.
        """
        seconds = Decimal(60) / Decimal(bpm_for_unit)
        self.seconds_per_fqmt = seconds


