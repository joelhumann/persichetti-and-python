# scales.py — Modal Systems and Interchange Tools

from typing import List, Dict, Optional

# --- Core Structures ---

class Scale:
    """
    Represents a generic scale type by name and pitch-class content.
    Pitch classes are relative to a tonic (assumed to be 0).
    """
    def __init__(
        self,
        name: str,
        pitch_classes: List[int],
        description: Optional[str] = None,
        category: Optional[str] = None,
        symmetric: Optional[bool] = None,
        multi_octave: bool = False
    ):
        self.name = name
        self.pitch_classes = sorted(set(pc % 12 for pc in pitch_classes))
        self.cardinality = len(self.pitch_classes)
        self.description = description
        self.category = category or self.infer_category()
        self.symmetric = symmetric if symmetric is not None else self.infer_symmetry()
        self.multi_octave = multi_octave

    def infer_category(self) -> str:
        """
        Infer the category based on the number of pitch classes.
        """
        categories = {
            5: "pentatonic",
            6: "hexatonic",
            7: "heptatonic",
            8: "octatonic",
            12: "dodecatonic"
        }
        return categories.get(self.cardinality, f"{self.cardinality}-tone")

    def infer_symmetry(self) -> bool:
        """
        Determines if the pitch class set is rotationally symmetric.
        """
        pcs = self.pitch_classes
        for shift in range(1, 12):
            rotated = sorted([(pc + shift) % 12 for pc in pcs])
            if rotated == pcs:
                return True
        return False


class ModalSystem:
    """
    Represents a mode: a specific tonicized realization of a scale.
    Also includes optional aliases and modal system membership.
    """
    def __init__(
        self,
        tonic: int,
        scale: Scale,
        aliases: Optional[List[str]] = None,
        as_mode_of: Optional[str] = None
    ):
        self.tonic = tonic % 12
        self.scale = scale
        self.aliases = aliases or []
        self.as_mode_of = as_mode_of
        self.triadic_hierarchy: Optional[Dict[str, any]] = None

    def degree_to_pc(self, degree: int) -> int:
        """
        Convert a scale degree (0-indexed) to absolute pitch class.
        """
        return (self.tonic + self.scale.pitch_classes[degree % self.scale.cardinality]) % 12

    def pc_to_degree(self, pc: int) -> Optional[int]:
        """
        Convert an absolute pitch class to degree within this mode.
        Returns None if not in scale.
        """
        rel_pc = (pc - self.tonic) % 12
        if rel_pc in self.scale.pitch_classes:
            return self.scale.pitch_classes.index(rel_pc)
        return None

    def absolute_pitch_classes(self) -> set:
        """
        Returns the set of absolute pitch classes for this mode.
        """
        return {(self.tonic + pc) % 12 for pc in self.scale.pitch_classes}
# --- Roman Numeral Utilities (Heptatonic Only) ---

def degree_to_roman(degree: int, mode: ModalSystem) -> Optional[str]:
    """
    Given a scale degree (0-indexed), return the Roman numeral with chord quality
    based on triadic construction: major, minor, diminished, or augmented.
    """
    if mode.scale.cardinality != 7:
        return None

    root = mode.degree_to_pc(degree)
    third = mode.degree_to_pc((degree + 2) % 7)
    fifth = mode.degree_to_pc((degree + 4) % 7)

    interval_3rd = (third - root) % 12
    interval_5th = (fifth - root) % 12

    numeral = ["I", "II", "III", "IV", "V", "VI", "VII"][degree]

    if interval_3rd == 4 and interval_5th == 7:
        return numeral
    elif interval_3rd == 3 and interval_5th == 7:
        return numeral.lower()
    elif interval_3rd == 3 and interval_5th == 6:
        return numeral.lower() + "°"
    elif interval_3rd == 4 and interval_5th == 8:
        return numeral + "+"
    else:
        return numeral + "(?)"


def roman_to_degree(roman: str, mode: ModalSystem) -> Optional[int]:
    """
    Convert Roman numeral (with ° or +) to a scale degree index.
    Assumes a heptatonic modal system.
    """
    if mode.scale.cardinality != 7:
        return None

    base = roman.replace("°", "").replace("+", "").upper()
    mapping = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4, "VI": 5, "VII": 6}
    return mapping.get(base)


# --- ModalTransformer ---

class ModalTransformer:
    """
    Enables modal interchange, modulation, and transformation across a collection of modal systems.
    """
    def __init__(self, *modal_dicts: Dict[str, ModalSystem]):
        self.modal_families = self.group_modal_systems_by_scale_type(*modal_dicts)
        self.all_modes: Dict[str, ModalSystem] = {}
        for d in modal_dicts:
            self.all_modes.update(d)

    def group_modal_systems_by_scale_type(self, *modal_dicts: Dict[str, ModalSystem]) -> Dict[str, Dict[str, ModalSystem]]:
        """
        Group ModalSystem instances by their parent scale type.
        """
        grouped: Dict[str, Dict[str, ModalSystem]] = {}
        for modal_dict in modal_dicts:
            for name, mode in modal_dict.items():
                if mode.as_mode_of:
                    grouped.setdefault(mode.as_mode_of, {})[name] = mode
        return grouped

    def modal_interchange(self, source: ModalSystem, target_mode_name: str) -> Optional[ModalSystem]:
        """
        Change mode name but preserve tonic. Returns new ModalSystem or None.
        """
        for name, mode in self.all_modes.items():
            if name == target_mode_name and mode.tonic == source.tonic:
                return mode
        return None

    def modal_modulation(self, source: ModalSystem, new_tonic: int) -> ModalSystem:
        """
        Change tonic while preserving mode identity.
        """
        return ModalSystem(
            tonic=new_tonic,
            scale=source.scale,
            aliases=source.aliases,
            as_mode_of=source.as_mode_of
        )

    def full_modal_transformation(
        self,
        source: ModalSystem,
        new_mode_name: Optional[str] = None,
        new_tonic: Optional[int] = None
    ) -> Optional[ModalSystem]:
        """
        Optional mode and/or tonic change. Returns new ModalSystem or None.
        """
        if new_mode_name:
            target_mode = self.all_modes.get(new_mode_name)
            if not target_mode:
                return None
            tonic = new_tonic if new_tonic is not None else source.tonic
            return ModalSystem(
                tonic=tonic,
                scale=target_mode.scale,
                aliases=target_mode.aliases,
                as_mode_of=target_mode.as_mode_of
            )
        elif new_tonic is not None:
            return self.modal_modulation(source, new_tonic)
        return source
# --- Diatonic Scale and Modes (Heptatonic) ---

DIATONIC_SCALE = Scale("Diatonic", [0, 2, 4, 5, 7, 9, 11], category="heptatonic", description="Standard major scale")

DIATONIC_MODES: Dict[str, ModalSystem] = {
    "Ionian":     ModalSystem(0, DIATONIC_SCALE, aliases=["Major"], as_mode_of="Diatonic"),
    "Dorian":     ModalSystem(2, DIATONIC_SCALE, as_mode_of="Diatonic"),
    "Phrygian":   ModalSystem(4, DIATONIC_SCALE, as_mode_of="Diatonic"),
    "Lydian":     ModalSystem(5, DIATONIC_SCALE, as_mode_of="Diatonic"),
    "Mixolydian": ModalSystem(7, DIATONIC_SCALE, as_mode_of="Diatonic"),
    "Aeolian":    ModalSystem(9, DIATONIC_SCALE, aliases=["Natural Minor"], as_mode_of="Diatonic"),
    "Locrian":    ModalSystem(11, DIATONIC_SCALE, as_mode_of="Diatonic"),
}


# --- Persichetti's Triadic Hierarchies for Diatonic Modes ---

DIATONIC_TRIADIC_HIERARCHIES: Dict[str, Dict[str, any]] = {
    "Dorian": {
        "tonic": "i",
        "primary": ["i", "ii", "IV"],
        "secondary": ["III", "v", "VII"],
        "diminished": "vi°",
        "notes": "Primary chords emphasize the raised 6th (A natural in C Dorian), found in ii and IV."
    },
    "Phrygian": {
        "tonic": "i",
        "primary": ["i", "II", "vii"],
        "secondary": ["III", "iv", "VI"],
        "diminished": "v°",
        "notes": "Primary chords emphasize the flat 2nd (Db in C Phrygian), in II and i. V° is treated carefully."
    },
    "Lydian": {
        "tonic": "I",
        "primary": ["I", "II", "vii"],
        "secondary": ["iii", "v", "vi"],
        "diminished": "iv°",
        "notes": "Primary chords emphasize the raised 4th (F# in C Lydian), found in II and vii."
    },
    "Mixolydian": {
        "tonic": "I",
        "primary": ["I", "vii", "v"],
        "secondary": ["ii", "iii", "vi"],
        "diminished": "iv°",
        "notes": "Primary chords emphasize the flat 7th (Bb in C Mixolydian), found in vii and v."
    },
    "Ionian": {
        "tonic": "I",
        "primary": ["I", "IV", "V"],
        "secondary": ["ii", "iii", "vi"],
        "diminished": "vii°",
        "notes": "Standard tonal hierarchy: tonic, subdominant, dominant. Functional harmony using leading tone."
    },
    "Aeolian": {
        "tonic": "i",
        "primary": ["i", "iv", "v"],
        "secondary": ["III", "VI", "VII"],
        "diminished": "ii°",
        "notes": "Natural minor harmonic structure. V remains minor (no raised leading tone)."
    }
}

# --- Attach hierarchies to modes ---
for name, mode in DIATONIC_MODES.items():
    if name in DIATONIC_TRIADIC_HIERARCHIES:
        mode.triadic_hierarchy = DIATONIC_TRIADIC_HIERARCHIES[name]
# --- Melodic Minor Scale and Modes (Jazz Ascending Form) ---

MELODIC_MINOR_SCALE = Scale(
    "Melodic Minor",
    [0, 2, 3, 5, 7, 9, 11],
    category="heptatonic",
    description="Jazz melodic minor (ascending)"
)

MELODIC_MINOR_MODES: Dict[str, ModalSystem] = {
    "Melodic Minor":        ModalSystem(0, MELODIC_MINOR_SCALE, as_mode_of="Melodic Minor"),
    "Dorian b2":            ModalSystem(2, MELODIC_MINOR_SCALE, as_mode_of="Melodic Minor"),
    "Lydian Augmented":     ModalSystem(4, MELODIC_MINOR_SCALE, as_mode_of="Melodic Minor"),
    "Overtone":             ModalSystem(5, MELODIC_MINOR_SCALE, aliases=["Lydian Dominant"], as_mode_of="Melodic Minor"),
    "Mixolydian b6":        ModalSystem(7, MELODIC_MINOR_SCALE, as_mode_of="Melodic Minor"),
    "Locrian ♮2":           ModalSystem(9, MELODIC_MINOR_SCALE, as_mode_of="Melodic Minor"),
    "Super Locrian":        ModalSystem(11, MELODIC_MINOR_SCALE, aliases=["Altered"], as_mode_of="Melodic Minor"),
}


# --- Harmonic Minor Scale and Modes (Classical Source) ---

HARMONIC_MINOR_SCALE = Scale(
    "Harmonic Minor",
    [0, 2, 3, 5, 7, 8, 11],
    category="heptatonic",
    description="Classical harmonic minor"
)

HARMONIC_MINOR_MODES: Dict[str, ModalSystem] = {
    "Harmonic Minor":        ModalSystem(0, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
    "Locrian ♮6":            ModalSystem(2, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
    "Ionian ♯5":             ModalSystem(4, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
    "Dorian ♯4":             ModalSystem(5, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
    "Phrygian Dominant":     ModalSystem(7, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
    "Lydian ♯2":             ModalSystem(9, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
    "Super Locrian ♭♭7":     ModalSystem(11, HARMONIC_MINOR_SCALE, as_mode_of="Harmonic Minor"),
}
# --- Synthetic Heptatonic Scale Types (Exotic Modes) ---

NEAPOLITAN_MINOR_SCALE = Scale("Neapolitan Minor", [0, 1, 3, 5, 7, 8, 11], category="heptatonic")
NEAPOLITAN_MAJOR_SCALE = Scale("Neapolitan Major", [0, 1, 3, 5, 7, 9, 11], category="heptatonic")
ORIENTAL_SCALE = Scale("Oriental", [0, 1, 4, 5, 6, 9, 10], category="heptatonic")
DOUBLE_HARMONIC_SCALE = Scale("Double Harmonic", [0, 1, 3, 5, 7, 8, 11], category="heptatonic")
ENIGMATIC_SCALE = Scale("Enigmatic", [0, 1, 4, 6, 8, 10, 11], category="heptatonic")
HUNGARIAN_MINOR_SCALE = Scale("Hungarian Minor", [0, 2, 3, 6, 7, 8, 11], category="heptatonic")
LEADING_WHOLETONE_SCALE = Scale("Leading Whole-Tone", [0, 2, 4, 6, 8, 10, 11], category="heptatonic")
HUNGARIAN_MAJOR_SCALE = Scale("Hungarian Major", [0, 3, 4, 6, 7, 9, 10], category="heptatonic")

# --- Generic Mode Builder ---

SYNTHETIC_MODES: Dict[str, ModalSystem] = {}

def add_synthetic_modes(name: str, scale: Scale, degrees: List[int]):
    for i, tonic in enumerate(degrees):
        label = name if i == 0 else f"{i+1}th mode of {name}"
        SYNTHETIC_MODES[label] = ModalSystem(tonic, scale, as_mode_of=name)

# --- Add modal systems for each synthetic scale ---

add_synthetic_modes("Neapolitan Minor", NEAPOLITAN_MINOR_SCALE, [0, 1, 3, 5, 7, 8, 11])
add_synthetic_modes("Neapolitan Major", NEAPOLITAN_MAJOR_SCALE, [0, 1, 3, 5, 7, 9, 11])
add_synthetic_modes("Oriental", ORIENTAL_SCALE, [0, 1, 4, 5, 6, 9, 10])
add_synthetic_modes("Double Harmonic", DOUBLE_HARMONIC_SCALE, [0, 1, 3, 5, 7, 8, 11])
add_synthetic_modes("Enigmatic", ENIGMATIC_SCALE, [0, 1, 4, 6, 8, 10, 11])
add_synthetic_modes("Hungarian Minor", HUNGARIAN_MINOR_SCALE, [0, 2, 3, 6, 7, 8, 11])
add_synthetic_modes("Leading Whole-Tone", LEADING_WHOLETONE_SCALE, [0, 2, 4, 6, 8, 10, 11])
add_synthetic_modes("Hungarian Major", HUNGARIAN_MAJOR_SCALE, [0, 3, 4, 6, 7, 9, 10])
# --- Pentatonic Scale Types ---

PENTATONIC_DIATONIC_SCALE = Scale("Diatonic Pentatonic", [0, 2, 4, 7, 9], category="pentatonic")
PELOG_SCALE = Scale("Pelog", [0, 1, 3, 7, 8], category="pentatonic")
HIRAJOSHI_SCALE = Scale("Hirajoshi", [0, 2, 3, 7, 8], category="pentatonic")
KUMOI_SCALE = Scale("Kumoi", [0, 2, 3, 7, 9], category="pentatonic")

DIATONIC_PENTATONIC_MODES: Dict[str, ModalSystem] = {
    "1st mode of Diatonic Pentatonic": ModalSystem(0, PENTATONIC_DIATONIC_SCALE, aliases=["Major Pentatonic"], as_mode_of="Diatonic Pentatonic"),
    "2nd mode of Diatonic Pentatonic": ModalSystem(2, PENTATONIC_DIATONIC_SCALE, as_mode_of="Diatonic Pentatonic"),
    "3rd mode of Diatonic Pentatonic": ModalSystem(4, PENTATONIC_DIATONIC_SCALE, as_mode_of="Diatonic Pentatonic"),
    "4th mode of Diatonic Pentatonic": ModalSystem(7, PENTATONIC_DIATONIC_SCALE, as_mode_of="Diatonic Pentatonic"),
    "5th mode of Diatonic Pentatonic": ModalSystem(9, PENTATONIC_DIATONIC_SCALE, aliases=["Minor Pentatonic"], as_mode_of="Diatonic Pentatonic"),
}


# --- Hexatonic Scale Types ---

SIX_TONE_SYMMETRICAL_SCALE = Scale("Six-Tone Symmetrical", [0, 1, 4, 5, 8, 9], category="hexatonic", symmetric=False)
PROMETHEUS_SCALE = Scale("Prometheus", [0, 2, 4, 6, 9, 10], category="hexatonic", symmetric=False)
PROMETHEUS_NEAPOLITAN_SCALE = Scale("Prometheus Neapolitan", [0, 1, 4, 6, 9, 10], category="hexatonic", symmetric=False)
WHOLE_TONE_SCALE = Scale("Whole-Tone", [0, 2, 4, 6, 8, 10], category="hexatonic", symmetric=True)


# --- Octatonic Scales ---

SYMMETRICAL_SCALE = Scale("Symmetrical", [0, 1, 3, 4, 6, 7, 9, 10], category="octatonic", symmetric=True)
EIGHT_TONE_SPANISH_SCALE = Scale("Eight-Tone Spanish", [0, 1, 3, 4, 5, 6, 8, 10], category="octatonic", symmetric=False)

# Aliased modal entries for symmetrical octatonics
HALF_WHOLE_DIMINISHED = ModalSystem(0, SYMMETRICAL_SCALE, aliases=["Half-Whole Diminished"], as_mode_of="Symmetrical")
WHOLE_HALF_DIMINISHED = ModalSystem(1, SYMMETRICAL_SCALE, aliases=["Whole-Half Diminished"], as_mode_of="Symmetrical")


# --- Chromatic Scale (12-tone) ---

CHROMATIC_SCALE = Scale("Chromatic", list(range(12)), category="dodecatonic", symmetric=True)
# --- User-Defined Scale Registries ---

USER_DEFINED_SCALES: Dict[str, Scale] = {}
"""
Stores user-defined scales. Differentiates multi-octave via the `multi_octave` flag in Scale object.
"""

USER_DEFINED_ALIASES: Dict[str, str] = {}
"""
Maps user-defined aliases to canonical scale names. Core definitions remain unmodified.
"""


# --- Add a User-Defined Scale ---

def add_user_defined_scale(
    name: str,
    pitch_classes: List[int],
    aliases: Optional[List[str]] = None,
    multi_octave: bool = False
) -> Optional[str]:
    """
    Add a new scale if it's not already present in any registry.
    If the pitch class set exists, only new aliases are registered.
    """
    normalized = sorted(set(pc % 12 for pc in pitch_classes))

    # Check predefined scales
    for scale in [
        DIATONIC_SCALE, MELODIC_MINOR_SCALE, HARMONIC_MINOR_SCALE,
        DOUBLE_HARMONIC_SCALE, ENIGMATIC_SCALE, NEAPOLITAN_MINOR_SCALE, NEAPOLITAN_MAJOR_SCALE,
        HUNGARIAN_MINOR_SCALE, HUNGARIAN_MAJOR_SCALE, LEADING_WHOLETONE_SCALE,
        ORIENTAL_SCALE, SYMMETRICAL_SCALE, WHOLE_TONE_SCALE, PROMETHEUS_SCALE,
        PROMETHEUS_NEAPOLITAN_SCALE, SIX_TONE_SYMMETRICAL_SCALE,
        PENTATONIC_DIATONIC_SCALE, PELOG_SCALE, HIRAJOSHI_SCALE, KUMOI_SCALE,
        EIGHT_TONE_SPANISH_SCALE, CHROMATIC_SCALE
    ]:
        if sorted(scale.pitch_classes) == normalized:
            if aliases:
                for alias in aliases:
                    USER_DEFINED_ALIASES[alias] = scale.name
            return scale.name

    # Check user-defined registry
    for existing in USER_DEFINED_SCALES.values():
        if sorted(existing.pitch_classes) == normalized:
            if aliases:
                for alias in aliases:
                    USER_DEFINED_ALIASES[alias] = existing.name
            return existing.name

    # Store new user-defined scale
    scale = Scale(name, normalized, multi_octave=multi_octave)
    USER_DEFINED_SCALES[name] = scale
    if aliases:
        for alias in aliases:
            USER_DEFINED_ALIASES[alias] = name
    return name
# --- Multi-Octave Scale Construction Tools ---

def build_multi_octave_scale_from_tetrachords(name: str, tetrachords: List[List[int]]) -> Scale:
    """
    Constructs a multi-octave scale from a list of tetrachords.
    Each tetrachord is a 4-note group (e.g. [0, 2, 4, 5]).
    All pitch classes are flattened into one merged scale.
    """
    pitch_classes = []
    for tet in tetrachords:
        pitch_classes.extend(tet)
    unique_pcs = sorted(set(pc % 12 for pc in pitch_classes))
    scale = Scale(name, unique_pcs, category="multi-octave", multi_octave=True)
    USER_DEFINED_SCALES[name] = scale
    return scale


def build_composite_scale(name: str, scale_a: Scale, scale_b: Scale) -> Scale:
    """
    Constructs a multi-octave scale by merging two one-octave scales
    assumed to share a tonic. Duplicate tones are eliminated.
    """
    combined_pcs = sorted(set(scale_a.pitch_classes + scale_b.pitch_classes))
    scale = Scale(name, combined_pcs, category="multi-octave", multi_octave=True)
    USER_DEFINED_SCALES[name] = scale
    return scale

from itertools import combinations
from typing import Tuple

# --- Tritone Detection Utility ---

def has_tritone(pitch_classes: List[int]) -> bool:
    """
    Returns True if any interval between two notes is a tritone (6 semitones).
    """
    pcs = sorted(pc % 12 for pc in pitch_classes)
    for a, b in combinations(pcs, 2):
        if abs((a - b) % 12) == 6:
            return True
    return False


# --- Chord Construction ---

def build_chord_from_degree(mode: ModalSystem, degree: int, extension: int = 3) -> List[int]:
    """
    Build a chord of given extension (3, 4, or 5 notes) from a scale degree.
    - 3 = triad (1–3–5)
    - 4 = seventh chord (1–3–5–7)
    - 5 = ninth chord (1–3–5–7–9)
    """
    intervals = [0, 2, 4, 6, 8][:extension]  # scale degrees offsets
    chord = [mode.degree_to_pc((degree + i) % mode.scale.cardinality) for i in intervals]
    return chord


# --- Diatonic Modal Chord Suggestion (Persichetti Logic) ---

def suggest_modal_chords_diatonic(mode: ModalSystem) -> List[Tuple[str, List[int], str]]:
    """
    Suggests triads, 7th chords, and 9th chords from a diatonic mode.
    Flags chords containing a tritone, which Persichetti advises against in modal contexts.

    Returns:
        A list of (label, pitch class list, safety marker)
    """
    if mode.as_mode_of != "Diatonic":
        raise ValueError("This function only supports diatonic modes.")

    suggestions = []

    for degree in range(mode.scale.cardinality):
        roman = degree_to_roman(degree, mode) or f"{degree + 1}"
        for ext in [3, 4, 5]:  # triads, 7ths, 9ths
            chord = build_chord_from_degree(mode, degree, ext)
            label = f"{roman}{'7' if ext == 4 else '9' if ext == 5 else ''}"
            if has_tritone(chord):
                suggestions.append((label, chord, "⚠️ contains tritone"))
            else:
                suggestions.append((label, chord, "✅ modal-safe"))
    return suggestions

# --- Modal Brightness Utility (Diatonic System Only) ---

DIATONIC_BRIGHTNESS_SCALE = {
    "Locrian":    -3,
    "Phrygian":   -2,
    "Aeolian":    -1,
    "Dorian":      0,
    "Mixolydian": +1,
    "Ionian":     +2,
    "Lydian":     +3
}

def modal_brightness(mode: ModalSystem) -> Optional[int]:
    """
    Returns a relative brightness index for a Diatonic mode.
    -3 = darkest (Locrian)
    +3 = brightest (Lydian)
    Returns None if the mode is not part of the Diatonic system.
    """
    name = next((k for k, v in DIATONIC_MODES.items() if v.tonic == mode.tonic), None)
    if name is None:
        return None
    return DIATONIC_BRIGHTNESS_SCALE.get(name)

# --- Chromatic Alteration of Diminished Triads (Diatonic Modes Only) ---

def suggest_diminished_alterations(mode: ModalSystem) -> Optional[Dict]:
    """
    Given a diatonic mode, identifies the diminished triad and suggests chromatic alterations
    that stabilize the tritone (either by raising the fifth or lowering the root).
    
    Returns:
        A dictionary with the original triad and its chromatic variants.
    """
    name = next((k for k, v in DIATONIC_MODES.items() if v.tonic == mode.tonic), None)
    if not name or name not in DIATONIC_TRIADIC_HIERARCHIES:
        return None  # Not a supported diatonic mode

    diminished_roman = DIATONIC_TRIADIC_HIERARCHIES[name].get("diminished")
    degree = roman_to_degree(diminished_roman, mode)
    if degree is None:
        return None

    # Build original diminished triad
    root = mode.degree_to_pc(degree)
    third = mode.degree_to_pc((degree + 2) % 7)
    fifth = mode.degree_to_pc((degree + 4) % 7)
    original = [root, third, fifth]

    # Alteration 1: raise the 5th (augmented fifth = major triad or dom7 base)
    raised_fifth = (fifth + 1) % 12
    alt1 = sorted([root, third, raised_fifth])

    # Alteration 2: lower the root (stabilizes 5th to a perfect 5th)
    lowered_root = (root - 1) % 12
    alt2 = sorted([lowered_root, third, fifth])

    return {
        "mode": name,
        "original_diminished": original,
        "alteration_raise_5th": {
            "chord": alt1,
            "comment": "Raises diminished 5th → stabilizes to major/minor triad or dominant variant"
        },
        "alteration_lower_root": {
            "chord": alt2,
            "comment": "Lowers root → forms new dominant-function triad"
        }
    }

# --- Locrian Tonic Voicing Suggestions (Avoiding Tritone) ---

def locrian_tonic_voicing_suggestions(mode: ModalSystem) -> Optional[Dict]:
    """
    Provides voicing alternatives for the Locrian tonic chord
    to avoid emphasizing the tritone.

    Suggestions include:
    - Omission of the fifth
    - Omission of third and fifth (unison/octave effect)
    - First inversion (3rd in the bass)
    """
    name = next((k for k, v in DIATONIC_MODES.items() if v.tonic == mode.tonic), None)
    if name != "Locrian":
        return None

    root = mode.degree_to_pc(0)
    third = mode.degree_to_pc(2)
    fifth = mode.degree_to_pc(4)

    diminished_triad = [root, third, fifth]

    return {
        "mode": "Locrian",
        "tonic_diminished_triad": diminished_triad,
        "suggestion_omit_5th": {
            "voicing": [root, third],
            "comment": "Removes tritone between root and diminished fifth"
        },
        "suggestion_omit_3rd_and_5th": {
            "voicing": [root],
            "comment": "Tonic stated in unison or octave only — no tritone present"
        },
        "suggestion_first_inversion": {
            "voicing": [third, root, fifth],
            "comment": "Tritone effect is subdued by placing 3rd in the bass"
        }
    }

# --- Locrian Tritone as Thematic Element ---

def locrian_tritone_themes(mode: ModalSystem) -> Optional[Dict]:
    """
    Given a Locrian mode, suggest melodic and harmonic patterns that emphasize the 
    tritone relationship between the tonic (I) and the fifth scale step (V).

    This highlights the use of the diminished fifth and its thematic potential in Locrian.
    Returns suggestions for melodic emphasis of the tritone.
    """
    name = next((k for k, v in DIATONIC_MODES.items() if v.tonic == mode.tonic), None)
    if name != "Locrian":
        return None  # Only works for Locrian mode

    # Get the tonic and fifth scale degree
    tonic = mode.degree_to_pc(0)
    fifth = mode.degree_to_pc(4)
    
    # Melodic pattern 1: Emphasize the tritone between tonic and fifth (in unison/octave)
    tritone_melodic = [tonic, fifth]

    # Melodic pattern 2: Use tonic and dominant 7th (tritone relationship still present)
    dominant_7th = [tonic, fifth, mode.degree_to_pc(3), mode.degree_to_pc(6)]  # Tonic, 5th, b7

    # Melodic pattern 3: Use both tonic and fifth in unison (obliterates tritone tension)
    unison_tonic_fifth = [tonic, tonic]  # Tonic and octave

    return {
        "mode": "Locrian",
        "tritone_melodic": {
            "pattern": tritone_melodic,
            "comment": "Melodic use of tonic and fifth, highlighting the tritone."
        },
        "dominant_7th_melodic": {
            "pattern": dominant_7th,
            "comment": "Dominant 7th with tonic and fifth, keeping tritone tension intact."
        },
        "unison_tonic_fifth": {
            "pattern": unison_tonic_fifth,
            "comment": "Tonic repeated in unison, removing tritone tension."
        }
    }
