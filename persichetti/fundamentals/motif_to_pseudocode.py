from typing import Dict, Any, List, Union
from .melodic_motif import MelodicMotif
from .event import Note, Rest

def motif_to_pseudocode(motif: MelodicMotif) -> Dict[str, Any]:
    """
    Converts a MelodicMotif into a fully descriptive pseudocode dictionary.
    This includes:
    - List of elements with type, pitch, duration, is_pitched
    - is_rhythmic status
    - pitch_context (as repr string)
    - total_duration if rhythmic
    - normalization status (heuristic)
    """
    elements_data: List[Dict[str, Union[str, int, None, bool]]] = []

    for el in motif.elements:
        if isinstance(el, Rest):
            kind = "rest"
            entry = {
                "type": kind,
                "pitch": None,
                "duration": el.duration,
                "is_pitched": False
            }

        elif isinstance(el, Note):
            kind = "xnote" if el.pitch is None else "note"
            entry = {
                "type": kind,
                "pitch": el.pitch,
                "duration": el.duration,
                "is_pitched": el.is_pitched()
            }

        else:
            raise TypeError(f"Unknown element type: {type(el)}")

        elements_data.append(entry)

    return {
        "elements": elements_data,
        "is_rhythmic": motif.is_rhythmic(),
        "pitch_context": repr(motif.pitch_context) if motif.pitch_context else None,
        "total_duration": motif.total_duration,
        "normalized": getattr(motif, "normalize", True)
    }


