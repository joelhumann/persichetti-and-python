# test_imports.py

from persichetti.core.pitch import Pitch
from persichetti.core.intervals import Interval
from persichetti.core.tuning import print_tuning_summary, TUNING
from persichetti.branches.tuning_systems.equal_temperament import EqualTemperament

def main():
    print("✅ Core imports successful.")

    # Test pitch creation and tuning
    p = Pitch(60)  # Middle C
    print(f"Pitch created: {p}")
    print(f"Frequency (from TUNING): {p.frequency():.2f} Hz")

    # Check tuning info
    print("\nTuning summary:")
    print_tuning_summary()

    # Test interval
    iv = Interval(7)
    print(f"\nInterval of 7 semitones: {iv}")

    # Swap tuning system dynamically
    new_tuning = EqualTemperament(base_freq=432.0, reference_note=("A", 4))
    freq = new_tuning.pitch_frequency(9, 4)  # A4
    print(f"\nTested alternate tuning system (A4 = 432 Hz): {freq:.2f} Hz")

if __name__ == "__main__":
    main()
