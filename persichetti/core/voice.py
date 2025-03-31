# voice.py

from typing import List, Optional
from .quantum_time import MusicalInertialFrame


class Voice:
    """
    Represents a single voice in the score, capable of being monophonic or polyphonic.
    Each voice is associated with a specific Musical Inertial Frame (MIF) for timing.
    """
    
    def __init__(self, name: str, mode: str, mif_handle: str = "default"):
        """
        Initialize a voice with a name, mode, and a default or provided MIF handle.
        
        :param name: The name of the voice.
        :param mode: The mode (e.g., 'Ionian', 'Dorian') of the voice.
        :param mif_handle: The handle for the MIF this voice will use (default is 'default').
        """
        self.name = name
        self.mode = mode
        self.mif_handle = mif_handle
        self.mif = None  # MIF will be assigned later
        self.events = []  # A list to store all events (motifs) for this voice
        self.instrument = None  # Placeholder for instrument assignment (optional)

    def assign_mif(self, mif_handle: str, mif_registry: dict):
        """
        Assign a Musical Inertial Frame (MIF) to this voice based on its mif_handle.
        If the MIF doesn't exist, create a new one.

        :param mif_handle: The handle to identify the MIF (e.g., 'default').
        :param mif_registry: The registry of all MIFs in the score, mapped by their handle.
        """
        if mif_handle in mif_registry:
            self.mif = mif_registry[mif_handle]  # Use the existing MIF
        else:
            # Create a new MIF if it doesn't exist
            self.mif = MusicalInertialFrame(tempo_function=None, start_time=None)
            mif_registry[mif_handle] = self.mif  # Store it in the registry

    def add_event(self, motif):
        """
        Add a melodic or harmonic motif to the voice's event list.

        :param motif: The motif to be added (either MelodicMotif or HarmonicMotif).
        """
        self.events.append(motif)

    def remove_event(self, motif):
        """
        Remove a motif from the voice's event list.

        :param motif: The motif to be removed.
        """
        if motif in self.events:
            self.events.remove(motif)

    def set_instrument(self, instrument):
        """
        Optionally set an instrument for this voice (if applicable).
        
        :param instrument: The instrument to be assigned to this voice.
        """
        self.instrument = instrument

    def __repr__(self):
        return f"Voice(name={self.name}, mode={self.mode}, mif_handle={self.mif_handle}, events={len(self.events)})"
