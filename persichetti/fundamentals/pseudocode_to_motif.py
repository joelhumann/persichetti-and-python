from typing import Dict, Any, List
from .event import Note, Rest
from .melodic_motif import MelodicMotif
from .pitch_context import PitchContext

def pseudocode_to_motif(pseudocode: Dict[str, Any]) -> MelodicMotif:
    """
    Reconstructs a MelodicMotif from dictionary-style pseudocode.
    Supports all types of elements (note, rest, xnote) and respects duration logic.
    """
    elements = []
    for entry in pseudocode["elements"]:
        kind = entry["type"]
        pitch = entry["pitch"]
        duration = entry["duration"]

        if kind == "rest":
            elements.append(Rest(duration))
        elif kind == "xnote":
            elements.append(Note(pitch=None, duration=duration))
        elif kind == "note":
            elements.append(Note(pitch=pitch, duration=duration))
        else:
            raise ValueError(f"Unknown element type: {kind}")

    pitch_context = None
    if pseudocode["pitch_context"]:
        # You can later replace this logic with a smarter deserializer
        pitch_context = PitchContext(pitch_source=None, tonicity=True)

    return MelodicMotif(
        elements=elements,
        pitch_context=pitch_context,
        normalize=pseudocode.get("normalized", True)
    )

