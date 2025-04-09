from melodic_motif import MelodicMotif, Note, Rest

def pseudocode_to_motif(pseudo: dict) -> MelodicMotif:
    """
    Converts a pseudomotif dictionary back into a MelodicMotif object.

    Ignores metadata fields like 'uuid', 'id', 'total_duration', 'normalized'.

    Args:
        pseudo (dict): A pseudomotif dictionary as produced by motif_to_pseudocode().

    Returns:
        MelodicMotif: A reconstructed motif with pitch context if present.
    """
    elements = []

    for entry in pseudo.get("elements", []):
        type_ = entry["type"]
        value = entry.get("value")
        duration = entry.get("duration")

        if type_ == "note":
            elements.append(Note(pitch=value, duration=duration))
        elif type_ == "xnote":
            elements.append(Note(pitch=value, duration=duration, xnote=True))
        elif type_ == "rest":
            elements.append(Rest(duration=duration))
        else:
            raise ValueError(f"Unknown pseudocode element type: {type_}")

    pitch_context = pseudo.get("pitch_context", None)

    return MelodicMotif(
        elements=elements,
        pitch_context=pitch_context,
        normalize=False  # assume already normalized when pseudocode was generated
    )
