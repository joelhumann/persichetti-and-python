# fundamentals/melodic_motif.py

from typing import List, Optional
from fundamentals.event import Element, Note, Rest
from fundamentals.pitch_context import PitchContext


class MelodicMotif:
    """
    Represents a monophonic sequence of musical elements (Notes and Rests).

    A MelodicMotif may be:
    - Free (no rhythmic duration): all elements must have duration=None.
    - Rhythmic (quantized in time): all elements must have an integer duration.

    A motif may include:
    - Pitched notes (with integer pitch values)
    - Unpitched notes (pitch=None)
    - Rests

    Pitched notes are interpreted in one of two ways:
    - With a PitchContext: validated against a pitch set (e.g., modal/tonal system)
    - Without a PitchContext: pitches are relative integers, normalized so the first pitched note is 0
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
        Enforces that all elements are either durational (integer) or free (None).
        """
        durations = [e.duration for e in self.elements]

        if all(d is None for d in durations):
            self.total_duration = None  # free motif
        elif all(isinstance(d, int) for d in durations):
            self.total_duration = sum(durations)  # rhythmic motif
        else:
            raise ValueError("Motif elements must be either all durational or all free.")

    def _normalize_pitches(self):
        """
        Enforces pitch validity and normalization:
        - If pitch_context is provided, validates that all pitches are allowed.
        - If no pitch_context, treats first pitched note as reference (pitch = 0)
          and adjusts other pitches as semitone offsets.
        """
        if not any(e.is_pitched() for e in self.elements):
            return  # no pitched notes to normalize

        if self.pitch_context:
            reference = self.pitch_context.get_reference(
                first_pitch=self._first_pitched_note()
            )
            for e in self.elements:
                if e.is_pitched():
                    if not self.pitch_context.is_allowed(e.pitch):
                        raise ValueError(f"Pitch {e.pitch} not allowed in pitch context.")
        else:
            # Re-center all pitched notes so that first becomes 0
            ref = self._first_pitched_note()
            for e in self.elements:
                if e.is_pitched():
                    e.pitch -= ref

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
        Returns True if the motif has a defined total duration.
        """
        return self.total_duration is not None

    def is_free(self) -> bool:
        """
        Returns True if the motif has no defined duration.
        """
        return self.total_duration is None

    def __repr__(self):
        kind = "Free" if self.is_free() else f"Duration: {self.total_duration}"
        context = repr(self.pitch_context) if self.pitch_context else "No Context"
        return f"<MelodicMotif {kind}, {len(self.elements)} elements, {context}>"

    def copy(self) -> "MelodicMotif":
        """
        Returns a deep copy of this MelodicMotif, including all elements.
        The pitch_context is shared (assumed immutable), but elements are copied.
        """
        new_elements = [e.copy() for e in self.elements]
        return MelodicMotif(
            elements=new_elements,
            pitch_context=self.pitch_context,
            normalize=False
        )
