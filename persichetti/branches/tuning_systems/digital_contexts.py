def midi_to_frequency(midi_note: int, reference=440.0) -> float:
    return reference * 2 ** ((midi_note - 69) / 12)

def frequency_to_midi(freq: float, reference=440.0) -> float:
    from math import log2
    return 69 + 12 * log2(freq / reference)