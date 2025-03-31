# motif.py

from typing import List


class MelodicMotif:
    """
    Represents a melodic motif, which can be either temporal (with rhythmic duration)
    or free-time (without rhythmic constraint).
    """

    def __init__(self, name: str, notes: List[str], is_temporal: bool = True, rhythm: Optional[List[float]] = None):
        """
        Initialize a melodic motif with a name, list of notes, temporal flag, and rhythm pattern.
        
        :param name: The name of the motif.
        :param notes: The list of notes (pitch names or pitch classes).
        :param is_temporal: Boolean flag indicating if the motif is temporal (has rhythm).
        :param rhythm: The rhythm pattern associated with the motif (for temporal motifs).
        """
        self.name = name
        self.notes = notes  # List of note names or pitch classes
        self.is_temporal = is_temporal
        self.rhythm = rhythm or []  # Rhythm pattern for temporal motifs

    def add_to_voice(self, voice: "Voice"):
        """
        Add the motif to a voice, ensuring compatibility with the voice's MIF (Musical Inertial Frame).
        
        :param voice: The voice to which the motif will be added.
        """
        if self.is_temporal and voice.mif_handle == "free-time":
            raise ValueError(f"Cannot add temporal motif to a free-time voice.")
        voice.add_event(self)

    def resolve_to_temporal(self):
        """
        Convert a free-time motif into a temporal motif by adding rhythmic durations to the notes.
        """
        if not self.is_temporal:
            raise ValueError("This motif is already temporal.")
        # Logic to resolve the free-time motif to a temporal one.
        self.is_temporal = True

    def __repr__(self):
        return f"MelodicMotif(name={self.name}, notes={self.notes}, is_temporal={self.is_temporal})"


class HarmonicMotif:
    """
    Represents a harmonic motif (a chord) that can be added to a voice.
    """
    def __init__(self, name: str, chord: List[str]):
        """
        Initialize a harmonic motif with a name and a list of notes (forming the chord).
        
        :param name: The name of the harmonic motif.
        :param chord: The chord (list of notes or pitch classes) that forms the motif.
        """
        self.name = name
        self.chord = chord  # A list of notes (or pitch classes) forming the chord

    def add_to_voice(self, voice: "Voice"):
        """
        Add the harmonic motif to a polyphonic or coupled monophonic voice.
        
        :param voice: The voice to which the harmonic motif will be added.
        """
        voice.add_event(self)

    def __repr__(self):
        return f"HarmonicMotif(name={self.name}, chord={self.chord})"
