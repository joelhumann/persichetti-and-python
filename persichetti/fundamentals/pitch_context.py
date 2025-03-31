# fundamentals/pitch_context.py

"""
Defines the PitchContext class for validating pitch types in a musical passage.

This class enforces which pitch classes (mod 12) are allowed, depending on
the provided scale/mode/user-defined set and the tonicity flag.
"""

from typing import Union, List, Optional, Set
from core.scales import Scale, ModalSystem


class PitchContext:
    def __init__(
        self,
        pitch_source: Union[Scale, ModalSystem, List[int]],
        tonicity: bool,
        reference_pitch: Optional[int] = None
    ):
        """
        Initialize the pitch context.

        Parameters:
        - pitch_source: defines the pitch-class environment.
            • If ModalSystem → tonicized, 0 is the tonic.
            • If Scale or List[int] → untonicized, 0 is just an element of the set.
        - tonicity: True if operating in a modal or tonal space; False if atonal or unordered.
        - reference_pitch: required only if tonicity is False and a runtime reference is needed.
        """
        self.tonicity = tonicity
        self.reference_pitch = reference_pitch

        if isinstance(pitch_source, ModalSystem):
            # ModalSystem includes tonality — we extract its tonicized pitch classes
            self.pitch_set = set(pitch_source.absolute_pitch_classes())

        elif isinstance(pitch_source, Scale):
            # A Scale is tonic-free — we take its pitch classes as-is
            self.pitch_set = set(pc % 12 for pc in pitch_source.pitch_classes)

        elif isinstance(pitch_source, list):
            # A user-defined list of pitch classes (can be raw semitones or mod 12)
            self.pitch_set = set(pc % 12 for pc in pitch_source)

        else:
            raise TypeError(
                "pitch_source must be a ModalSystem, Scale, or list of integers."
            )

    def is_allowed(self, pitch: int) -> bool:
        """
        Check whether the given pitch (as integer) is allowed in this context.
        Validity is based on %12 membership in the pitch_set.
        """
        return pitch % 12 in self.pitch_set
    
    def get_reference(self, first_pitch: Optional[int] = None) -> int:
        """
        Returns the reference pitch (the pitch considered '0').

        - If tonicity is True, returns 0 (tonic is 0).
        - If tonicity is False, returns:
            • reference_pitch (if provided during initialization), or
            • first_pitch (if passed in at runtime), or
            • raises ValueError if neither is available.
        """
        if self.tonicity:
            return 0
        if self.reference_pitch is not None:
            return self.reference_pitch
        if first_pitch is not None:
            return first_pitch
        raise ValueError("Tonicity is False but no reference_pitch or first_pitch provided.")

    def __repr__(self) -> str:
        tonic_status = "True" if self.tonicity else "False"
        pcs = sorted(self.pitch_set)
        return f"<PitchContext tonic={tonic_status} pitch_set={pcs}>"



