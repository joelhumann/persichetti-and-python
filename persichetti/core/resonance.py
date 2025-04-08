# resonance.py

from collections import defaultdict, Counter
from persichetti.fundamentals.pitch import Pitch
from .intervals import Interval
from itertools import combinations
import math

# --- 1. Overtone Series ---

class OvertoneSeries:
    """Generates the first N overtones of a fundamental frequency."""
    def __init__(self, base_freq=110.0, num_partials=16):
        self.base = base_freq
        self.num_partials = num_partials
        self.overtones = self._generate()

    def _generate(self):
        series = []
        for n in range(1, self.num_partials + 1):
            freq = self.base * n
            series.append((n, freq))
        return series

    def display(self):
        for n, f in self.overtones:
            print(f"{n:>2}: {f:.2f} Hz")

# --- 2. Suggest Resonant Supports ---

def suggest_supporting_tones(bass_pitch: Pitch):
    """
    Returns a list of pitches that lie a fifth and a ninth below the given pitch.
    These help reinforce overtone resonance.
    """
    fifth_below = Pitch(bass_pitch.index - 7)
    ninth_below = Pitch(bass_pitch.index - 14)
    return [fifth_below, ninth_below]

# --- 3. Brilliance Score ---

RESONANT_INTERVALS = {"oct", "P5", "P4", "maj3", "min3", "maj6"}

def brilliance_score(chord, context=None):
    """
    Returns a score for how well a chord's intervals align with overtone spacing.
    Higher score = more 'brilliant'.
    """
    score = 0
    for interval in chord.intervals:
        interval_type = interval.type
        if interval_type in RESONANT_INTERVALS:
            score += 1
    return score

# --- 4. Amplify Existing Overtones ---

def amplify_existing_overtones(chord, partials=8, tolerance_cents=25):
    """
    Suggests pitches that reinforce overlapping overtones in the chord.

    Returns:
        list of dict:
            Each dict has the following keys:

            - 'pitch': Pitch object
            - 'reinforced_by': list of (source_pitch, harmonic_number)
    """

    overtone_hits = defaultdict(list)
    existing_indices = set(p.index for p in chord.pitches)

    for source_pitch in chord.pitches:
        base_freq = source_pitch.frequency()
        for n in range(2, partials + 1):
            overtone_freq = base_freq * n
            overtone_index = round(12 * math.log2(overtone_freq / 440.0))  # ET index
            if overtone_index not in existing_indices:
                overtone_hits[overtone_index].append((source_pitch, n))

    # Only suggest tones that appear in multiple overtone sets
    suggestions = []
    for index, sources in overtone_hits.items():
        if len(sources) >= 2:
            suggestions.append({
                "pitch": Pitch(index),
                "reinforced_by": sources
            })

    return suggestions

# --- 5. Resonance Profile Summary ---

def resonance_profile(chord, context=None):
    """
    Prints a musical profile of the chord's resonance qualities.
    Includes:
    - Brilliance score
    - Suggested resonance supports
    - Suggested reinforcement tones with overtone sources
    """
    print("🎼 Resonance Profile")
    print("--------------------")
    print("Chord tones:", ", ".join([str(p) for p in chord.pitches]))

    # Brilliance
    score = brilliance_score(chord, context)
    print(f"\nBrilliance score: {score} (higher = more overtone-aligned)")

    # Supporting tones
    bass = min(chord.pitches, key=lambda p: p.index)
    supports = suggest_supporting_tones(bass)
    print(f"\nSuggested support tones below bass ({bass}):")
    for s in supports:
        print("  →", s)

    # Overtones to amplify
    suggestions = amplify_existing_overtones(chord)
    print("\nSuggested reinforcement tones (overlapping overtones):")
    for item in suggestions:
        print(f"  → {item['pitch']} reinforced by:")
        for src, harmonic in item["reinforced_by"]:
            print(f"     - {src} (harmonic {harmonic})")

