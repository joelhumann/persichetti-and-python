from typing import Dict, Any, List, Union
from uuid import uuid4
from melodic_motif import MelodicMotif, Note, Rest


def motif_to_pseudocode(motif: MelodicMotif, label: str = None) -> Dict[str, Any]:
    """
    Converts a MelodicMotif into a structured pseudomotif dictionary
    with rich metadata and musical information for rendering, analysis, or storage.

    Args:
        motif (MelodicMotif): The motif to convert.
        label (str, optional): Optional human-readable ID label.

    Returns:
        dict: A pseudomotif dictionary with the following fields:
            - "type": always "pseudomotif"
            - "id": optional label (can be None)
            - "uuid": unique identifier (string)
            - "duration_type": "free" or "rhythmic"
            - "pitch_context": PitchContext object or None
            - "elements": list of dicts (notes, rests, xnotes)
            - "total_duration": sum of all durations (float)
            - "normalized": whether the motif is normalized (bool)
    """
    elements_data: List[Dict[str, Union[str, int, float, None]]] = []

    for el in motif.elements:
        if isinstance(el, Rest):
            elements_data.append({
                "type": "rest",
                "value": None,
                "duration": el.duration
            })
        elif isinstance(el, Note):
            kind = "xnote" if getattr(el, "xnote", False) else "note"
            elements_data.append({
                "type": kind,
                "value": el.pitch,
                "duration": el.duration
            })
        else:
            raise TypeError(f"Unknown element type: {type(el)}")

    total_duration = sum(
        e["duration"] for e in elements_data
        if e.get("duration") is not None
    )

    return {
        "type": "pseudomotif",
        "id": label or None,
        "uuid": str(uuid4()),
        "duration_type": "free" if motif.is_free() else "rhythmic",
        "pitch_context": motif.get_pitch_context(),
        "elements": elements_data,
        "total_duration": total_duration,
        "normalized": getattr(motif, "normalized", True),
    }

