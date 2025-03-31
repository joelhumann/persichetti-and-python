"""
score_structure.py

Defines musical agents such as Voice, which operate within the temporal logic
defined in quantum_time.py. Voices are assigned to Musical Inertial Frames (MIFs),
allowing for synchronization or independence in temporal expression.
"""

from quantum_time import MusicalInertialFrame


class Voice:
    """
    Represents a musical voice or agent in the compositional system.

    Attributes:
        name (str): Label for the voice (e.g., "Violin I", "Bass Clarinet").
        mif (MusicalInertialFrame): The local temporal frame of reference.
        instrument (str): Identifier or instrument class reference.
        events (list): Musical events associated with this voice.

    Methods:
        set_instrument(instrument): Updates the instrument.
        add_event(event): Adds a musical event to the voice's timeline.
    """
    def __init__(self, name, mif: MusicalInertialFrame, instrument="default"):
        self.name = name
        self.mif = mif
        self.instrument = instrument
        self.events = []

    def set_instrument(self, instrument):
        """Change the instrument associated with this voice."""
        self.instrument = instrument

    def add_event(self, event):
        """Append a musical event to this voice."""
        self.events.append(event)

    def __repr__(self):
        return f"Voice(name={self.name}, instrument={self.instrument}, MIF={self.mif})"
