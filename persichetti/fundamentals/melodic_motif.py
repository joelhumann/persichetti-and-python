#fundamentals/melodic_motif.py

from typing import List, Optional, Union
from fractions import Fraction
from .event import Element, Note, Rest
from .pitch_context import PitchContext


class MelodicMotif:
    """
    Represents a monophonic sequence of musical elements (Notes and Rests).

    A MelodicMotif may be:
    - Free (unquantized): all elements must have duration=None.
    - Rhythmic (quantized): all elements must have a numerical duration,
      expressed in integer or fractional multiples of a quantum time unit.

    ------------------
    RHYTHMIC STRUCTURE:

    Durations may be:
    - Integer (e.g. 1, 2, 4) for simple subdivisions
    - Fractional (e.g. 2/3, 3/5, 7/8) for complex tuplets

    All durations must share a common interpretation via a quantum time unit
    (typically specified in a `TimeContext`).

    ------------------
    PITCH STRUCTURE:

    A motif may include:
    - Pitched notes (int)
    - Unpitched notes (pitch=None)
    - Rests (no pitch)

    Pitched notes are interpreted as:
    - Relative pitch classes (semitones) if `pitch_context` is None
    - Validated modal/tonal pitches if `pitch_context` is provided

    ------------------
    Example:
        [Note(0, Fraction(2, 3)), Note(2, Fraction(1, 3)), Rest(Fraction(1, 3))]
        → Tuplet-like rhythmic grouping (e.g. 3 in the time of 2)
    """

    def __init__(
        self,
        elements: List[Element],
        pitch_context: Optional[PitchContext] = None,
        normalize: bool = True
    ):
        self.elements = elements
        self.pitch_context = pitch_context

        self._validate_duration_consistency()

        if normalize:
            self._normalize_pitches()

    def _validate_duration_consistency(self):
        """
        Validates whether the motif is free or rhythmic.
        - Free: all elements must have duration=None
        - Rhythmic: all elements must have a numeric duration (int or Fraction)
        """
        durations = [e.duration for e in self.elements]

        if all(d is None for d in durations):
            self.total_duration = None  # Free motif
        elif all(isinstance(d, (int, Fraction)) for d in durations):
            self.total_duration = sum(Fraction(d) for d in durations)
        else:
            raise ValueError(
                "Motif elements must be either all durational (int or Fraction) or all free (None)."
            )

    def _normalize_pitches(self):
        """
        Enforces pitch normalization:
        - With a PitchContext: validates pitches
        - Without context: shifts first pitched note to pitch 0
        """
        if not any(e.is_pitched() for e in self.elements):
            return

        if self.pitch_context:
            reference = self.pitch_context.get_reference(
                first_pitch=self._first_pitched_note()
            )
            for e in self.elements:
                if e.is_pitched():
                    if not self.pitch_context.is_allowed(e.pitch):
                        raise ValueError(f"Pitch {e.pitch} not allowed in pitch context.")
        else:
            ref = self._first_pitched_note()
            for e in self.elements:
                if e.is_pitched():
                    e.pitch -= ref

    def normalize(self):
        """
        Re-applies pitch normalization.
        - With a context: validates all pitches
        - Without context: shifts first pitched note to 0
        """
        self._normalize_pitches()

    def _first_pitched_note(self) -> int:
        """
        Returns the pitch value of the first pitched note.
        Raises an error if there are no pitched notes.
        """
        for e in self.elements:
            if e.is_pitched():
                return e.pitch
        raise ValueError("No pitched notes in motif.")

    def get_pitches(self) -> List[Optional[int]]:
        """
        Returns a list of pitch values for each element.
        Unpitched notes and rests return None.
        """
        return [e.pitch if e.is_pitched() else None for e in self.elements]

    def is_rhythmic(self) -> bool:
        """
        Returns True if the motif has a defined rhythmic structure.
        """
        return self.total_duration is not None

    def is_free(self) -> bool:
        """
        Returns True if the motif has no durations (i.e., free rhythm).
        """
        return self.total_duration is None

    def get_pitch_context(self):
        """
        Returns the pitch context associated with the motif, or None if unset.
        """
        if self.pitch_context is not None and not isinstance(self.pitch_context, PitchContext):
            raise TypeError("pitch_context must be a PitchContext or None")
        return self.pitch_context

    def __repr__(self):
        kind = "Free" if self.is_free() else f"Duration: {self.total_duration}"
        context = repr(self.pitch_context) if self.pitch_context else "No Context"
        return f"<MelodicMotif {kind}, {len(self.elements)} elements, {context}>"

    def copy(self) -> "MelodicMotif":
        """
        Returns a deep copy of this MelodicMotif.
        The pitch_context is shared (assumed immutable), but all elements are copied.
        """
        new_elements = [e.copy() for e in self.elements]
        return MelodicMotif(
            elements=new_elements,
            pitch_context=self.pitch_context,
            normalize=False
        )
