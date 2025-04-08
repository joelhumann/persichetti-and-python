# intervals.py

# --- 1. Interval Types ---
INTERVAL_TYPES = {
    0:  ("oct",      "open consonance"),
    1:  ("min2",     "sharp dissonance"),
    2:  ("maj2",     "mild dissonance"),
    3:  ("min3",     "soft consonance"),
    4:  ("maj3",     "soft consonance"),
    5:  ("P4",       "indeterminate"),
    6:  ("tritone",  "indeterminate"),
    7:  ("P5",       "open consonance"),
    8:  ("min6",     "soft consonance"),
    9:  ("maj6",     "soft consonance"),
    10: ("min7",     "mild dissonance"),
    11: ("maj7",     "sharp dissonance")
}

# --- 2. Tension Rankings ---
DIATONIC_TENSION_RANK = {
    "oct": 1, "P5": 2, "P4": 3, "maj3": 4, "min6": 5, "min3": 6,
    "maj6": 7, "min7": 8, "maj2": 9, "maj7": 10, "min2": 11, "tritone": 12
}

CHROMATIC_TENSION_RANK = {
    "oct": 1, "P5": 2, "maj3": 3, "min3": 4, "maj6": 5, "min6": 6,
    "tritone": 7, "maj2": 8, "min7": 9, "P4": 10, "maj7": 11, "min2": 12
}

# --- 3. Textural Class ---
class TexturalClass:
    def __init__(self, label):
        self.label = label.lower()

    def is_consonant(self):
        return self.label in {"open consonance", "soft consonance"}

    def is_dissonant(self):
        return self.label in {"sharp dissonance", "mild dissonance"}

    def is_ambiguous(self):
        return self.label == "indeterminate"

    def resolve(self, interval_type, context):
        if interval_type == "tritone":
            return "neutral" if context.get("environment") == "chromatic" else "restless"
        elif interval_type == "P4":
            return "consonant" if context.get("environment") == "dissonant" else "dissonant"
        return self.label

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"TexturalClass('{self.label}')"

# --- 4. Spacing-aware Qualia Modification ---

# NOTE ON MEDIUM CONTEXT:
# This function includes optional logic for simulating how 'medium' (instrument family,
# register, etc.) influences intervallic qualia. These mappings are not systematic rules,
# but expressive approximations, inspired by Persichetti's observations in Chapter 1, Section 5.
# For instance, a minor 2nd played high in the violin range may feel 'brilliant', while
# the same interval low in the bassoon may feel 'muffled'.
# 
# This system is intended as a flexible and pedagogically useful 'hook' for experimentation,
# and can be extended or refined with empirical data, user-defined mappings, or orchestration heuristics.
def modify_qualia_for_spacing(base_qualia, interval_type, openness, context=None):
    if context:
        medium = context.get("medium", {})
        register = medium.get("register")
        instrument = medium.get("instrument_family")

        if base_qualia == "sharp dissonance" and register == "high":
            return "brilliant dissonance"
        if base_qualia == "sharp dissonance" and register == "low":
            return "muffled dissonance"
        if interval_type == "tritone" and instrument == "strings" and register == "high":
            return "icy"

    if openness == "compact":
        return base_qualia

    if base_qualia == "soft consonance":
        return "open consonance"
    if base_qualia == "mild dissonance":
        return "colorful dissonance"
    if base_qualia == "sharp dissonance":
        return "brilliant dissonance"
    if base_qualia == "consonant" and interval_type == "P4":
        return "strong consonance"
    if base_qualia == "dissonant" and interval_type == "P4":
        return "brilliant dissonance"
    if base_qualia == "restless" and interval_type == "tritone":
        return "mildly restless"
    if base_qualia == "neutral" and interval_type == "tritone":
        return "veiled"

    return base_qualia

# --- 5. Interval Class ---
class Interval:
    def __init__(self, semitone_distance):
        self.spacing = semitone_distance
        mod12 = semitone_distance % 12
        self.type, raw_qualia = INTERVAL_TYPES[mod12]
        self.qualia = TexturalClass(raw_qualia)

    def resolve(self, context):
        return self.qualia.resolve(self.type, context)

    @property
    def degrees_apart(self):
        return self.spacing // 12

    @property
    def openness(self):
        if self.spacing <= 12:
            return "compact"
        elif self.spacing <= 24:
            return "wide"
        else:
            return "very wide"

    def spaced_qualia(self, context=None):
        base = self.resolve(context)
        return modify_qualia_for_spacing(base, self.type, self.openness, context)

    def invert(self):
        inverted_distance = 12 - (self.spacing % 12) if self.spacing % 12 != 0 else 0
        return Interval(inverted_distance)

    def tension_rank(self, context=None, custom_rank=None):
        if custom_rank:
            return custom_rank.get(self.type)
        if context and context.get("environment") == "chromatic":
            return CHROMATIC_TENSION_RANK.get(self.type)
        return DIATONIC_TENSION_RANK.get(self.type)

    def __repr__(self):
        return f"Interval({self.spacing}) = {self.type}, {self.qualia}, {self.openness}"

from itertools import combinations
from persichetti.fundamentals.pitch import Pitch

class Chord:
    def __init__(self, pitches: list[Pitch]):
        if len(pitches) < 2:
            raise ValueError("A chord must contain at least two pitches.")
        self.pitches = sorted(pitches, key=lambda p: p.index)
        self.intervals = self._generate_intervals()

    def _generate_intervals(self):
        intervals = []
        for a, b in combinations(self.pitches, 2):
            interval = Interval(b.index - a.index)
            intervals.append(interval)
        return intervals

    def qualia_profile(self, context=None):
        profile = {}
        for iv in self.intervals:
            q = iv.resolve(context)
            profile[q] = profile.get(q, 0) + 1
        return profile

    def resolve_all(self, context=None):
        return [iv.resolve(context) for iv in self.intervals]

    def __repr__(self):
        pcs = ', '.join([p.pc.name for p in self.pitches])
        return f"Chord([{pcs}])"

class Trichord(Chord):
    """Specialized class for 3-note chords with Persichetti-style classification."""

    def __init__(self, pitches: list[Pitch]):
        if len(pitches) != 3:
            raise ValueError("A Trichord must contain exactly 3 pitches.")
        super().__init__(pitches)

    def classify_trichord(self, context=None):
        resolved_qualia = {}
        for a, b in combinations(self.pitches, 2):
            interval = Interval(b.index - a.index)
            resolved = interval.resolve(context)
            resolved_qualia[(a, b)] = (interval.type, resolved)

        types = [res for _, res in resolved_qualia.values()]
        types_set = set(types)
        has_tritone = any(t == "tritone" for t, _ in resolved_qualia.values())
        has_sharp_dissonance = "sharp dissonance" in types_set

        p4_pair = None
        for (a, b), (typ, q) in resolved_qualia.items():
            if typ == "P4":
                p4_pair = (a, b)
                break

        if p4_pair:
            other = [p for p in self.pitches if p not in p4_pair][0]
            ref = p4_pair[0]
            ref_interval = Interval(abs(other.index - ref.index))
            other_qualia = ref_interval.resolve(context)

            if other_qualia in {"mild dissonance", "sharp dissonance"}:
                p4_reinterpreted = "open consonance"
            elif other_qualia in {"soft consonance"}:
                p4_reinterpreted = "mild dissonance"
            else:
                p4_reinterpreted = q

            types_set.discard("indeterminate")
            types_set.add(p4_reinterpreted)

        if "tritone" in [t for t, _ in resolved_qualia.values()]:
            return "restless"
        elif has_sharp_dissonance:
            return "tense stable"
        else:
            return "truly stable"

    def __repr__(self):
        pcs = ', '.join([p.pc.name for p in self.pitches])
        return f"Trichord([{pcs}])"
