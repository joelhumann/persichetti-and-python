from collections import Counter
from .intervals import Interval
from persichetti.fundamentals.pitch import Pitch, PitchClass
from itertools import combinations
from collections import Counter
import math

class ChordTexture:
    """Analyzes voicing and texture of a Chord."""

    def __init__(self, chord):
        self.chord = chord
        self.pitches = chord.pitches
        self.pitch_classes = [p.pc.value for p in self.pitches]
        self.intervals = chord.intervals

    def doubling_profile(self):
        """Returns a dictionary of pitch class counts."""
        return Counter(self.pitch_classes)

    def is_percussive(self):
        """
        Returns True if all pitch classes are doubled (or more),
        implying a percussive voicing style.
        """
        profile = self.doubling_profile()
        return all(count > 1 for count in profile.values())

    def interval_dominance(self):
        """
        Returns a frequency count of interval types in the chord.
        """
        type_counts = Counter()
        for interval in self.intervals:
            type_counts[interval.type] += 1
        return type_counts

    def clarity_score(self):
        """
        Returns a heuristic 'cloudiness' score:
        lower = clearer, higher = more clustered.
        Based on average interval spacing (in semitones).
        """
        if not self.intervals:
            return 0
        total_spacing = sum(iv.spacing for iv in self.intervals)
        average_spacing = total_spacing / len(self.intervals)
        # Invert: higher spacing = lower cloudiness
        return round(12 - average_spacing, 2)  # 12 as arbitrary norm

    def spacing_pattern(self):
        """
        Returns a rough pattern of spacing from bottom to top.
        Example: ['wide', 'close', 'wide']
        """
        pattern = []
        for i in range(len(self.pitches) - 1):
            spacing = self.pitches[i+1].index - self.pitches[i].index
            if spacing <= 4:
                pattern.append("tight")
            elif spacing <= 12:
                pattern.append("medium")
            else:
                pattern.append("wide")
        return pattern

    def summary(self):
        print(f"Chord: {', '.join([p.pc.name + str(p.index) for p in self.pitches])}")
        print("Doubling profile:", self.doubling_profile())
        print("Percussive:", self.is_percussive())
        print("Interval dominance:", self.interval_dominance())
        print("Clarity score (lower is clearer):", self.clarity_score())
        print("Spacing pattern (bottom to top):", self.spacing_pattern())

def amplify_existing_overtones(chord, partials=8, tolerance_cents=25):
    """
    Suggests additional pitches that would reinforce overlapping overtones in a chord.

    Returns a list of Pitch objects (not already in the chord) that would strengthen resonance.
    """
    overtone_bins = Counter()
    existing_indices = set(p.index for p in chord.pitches)

    # Collect overtone bins (rounded to nearest semitone)
    for pitch in chord.pitches:
        base_freq = pitch.frequency()
        for n in range(2, partials + 1):  # skip fundamental
            overtone_freq = base_freq * n
            overtone_index = round(12 * math.log2(overtone_freq / 440.0))  # map to ET index
            overtone_bins[overtone_index] += 1

    # Only keep tones that appear as overtones of multiple chord tones
    suggested = []
    for index, count in overtone_bins.items():
        if count >= 2 and index not in existing_indices:
            suggested.append(Pitch(index))

    return suggested
  
