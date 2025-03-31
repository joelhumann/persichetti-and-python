# score.py

from typing import Dict, List
from .quantum_time import MusicalInertialFrame, FQMTResolver
from .voice import Voice
from .motif import MelodicMotif, HarmonicMotif


class Score:
    """
    Represents the entire musical score, managing voices, motifs, and synchronization
    through Musical Inertial Frames (MIFs).
    """
    def __init__(self):
        self.voices: Dict[str, Voice] = {}  # Dictionary of voice names to Voice objects
        self.mif_registry: Dict[str, MusicalInertialFrame] = {}  # Registry of MIFs by handle
        self.events = []  # List to store all events in the score

    def add_voice(self, name: str, mode: str, mif_handle: str = "default"):
        """
        Add a new voice to the score, with a specified mode and MIF handle.
        If the voice already exists, it won't be added again.
        """
        if name not in self.voices:
            voice = Voice(name, mode, mif_handle)
            self.voices[name] = voice
            voice.assign_mif(mif_handle, self.mif_registry)
        else:
            print(f"Voice '{name}' already exists.")

    def add_motif_to_voice(self, voice_name: str, motif: MelodicMotif or HarmonicMotif):
        """
        Add a melodic or harmonic motif to a voice, ensuring it is compatible with the voice's MIF.
        """
        voice = self.voices.get(voice_name)
        if voice:
            motif.add_to_voice(voice)
            self.events.append(motif)  # Add to global event list
        else:
            print(f"Voice '{voice_name}' not found in the score.")

    def remove_motif_from_voice(self, voice_name: str, motif: MelodicMotif or HarmonicMotif):
        """
        Remove a motif from a voice in the score.
        """
        voice = self.voices.get(voice_name)
        if voice:
            if motif in voice.events:
                voice.events.remove(motif)
                self.events.remove(motif)
            else:
                print(f"Motif '{motif.name}' not found in voice '{voice_name}'.")
        else:
            print(f"Voice '{voice_name}' not found in the score.")

    def get_voice_events(self, voice_name: str) -> List:
        """
        Retrieve all events (motifs) associated with a specific voice.
        """
        voice = self.voices.get(voice_name)
        if voice:
            return voice.events
        return []

    def resolve_time(self):
        """
        Implement time logic for the score, adjusting timing based on MIFs.
        This method would interface with FQMTResolver and synchronize time across MIFs.
        """
        fqmt_resolver = FQMTResolver()
        # Add frames based on the MIFs of all voices
        for voice in self.voices.values():
            fqmt_resolver.add_frame(voice.mif, smallest_unit_in_beats=Fraction(1, 4))  # example unit
        fqmt = fqmt_resolver.compute_fqmt()

        # Update each voice's MIF with the global FQMT
        for voice in self.voices.values():
            voice.mif.tempo_function.set_tempo(fqmt)

    def __repr__(self):
        return f"Score(voices={len(self.voices)}, events={len(self.events)})"
