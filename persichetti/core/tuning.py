from typing import Optional, List
# core/tuning.py

import os

# Read environment variable to choose tuning
TUNING_SYSTEM = os.getenv("TUNING_SYSTEM", "equal").lower()

if TUNING_SYSTEM == "pythagorean":
    from persichetti.branches.tuning_systems.pythagorean import PythagoreanTuning
    TUNING = PythagoreanTuning(base_freq=261.63)

elif TUNING_SYSTEM == "just":
    from persichetti.branches.tuning_systems.just_intonation import JustIntonationZarlino
    TUNING = JustIntonationZarlino(base_freq=261.63)

elif TUNING_SYSTEM == "et_432":
    from persichetti.branches.tuning_systems.equal_temperament import EqualTemperament
    TUNING = EqualTemperament(base_freq=432.0, reference_note=("A", 4))

else:
    # Default: Equal Temperament with symbolic "golden key" base frequency (C4 = 261.63 Hz)
    from persichetti.branches.tuning_systems.equal_temperament import EqualTemperament
    TUNING = EqualTemperament(base_freq=440.0, reference_note=("A", 4))

# 🎼 Optional diagnostic utility
def print_tuning_summary(octave=4):
    """
    Prints the name of the current tuning system and the frequency of each pitch class in the given octave.
    """
    print(f"🎼 Current tuning system: {TUNING.name()} (octave {octave})")
    print("-" * 40)
    spellings = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    for pc in range(12):
        freq = TUNING.pitch_frequency(pc, octave)
        print(f"{spellings[pc]:>2} | {freq:.2f} Hz")
