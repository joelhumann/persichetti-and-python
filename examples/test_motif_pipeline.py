# examples/test_motif_pipeline.py

from pathlib import Path
import sys
import shutil
import pytest

lilypond_exists = shutil.which("lilypond") is not None

# Ensure persichetti/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from persichetti.fundamentals.event import Note, Rest
from persichetti.fundamentals.melodic_motif import MelodicMotif
from persichetti.fundamentals.pitch_context import PitchContext
from persichetti.fundamentals.resolver import LilypondResolver, TimeContext
from persichetti.fundamentals.motif_to_pseudocode import motif_to_pseudocode
from persichetti.core.scales import DIATONIC_MODES

# Step 1: Create a simple rhythmic motif
# These are semitone offsets from reference (0), NOT scale degrees
elements = [
    Note(pitch=0, duration=4),   # Reference pitch (0 semitones)
    Note(pitch=2, duration=4),   # +2 semitones from 0 (Dorian: D -> E)
    Rest(duration=2),           # Rest
    Note(pitch=5, duration=2),   # +5 semitones from 0 (Dorian: D -> G)
    Note(pitch=None, duration=4)  # Ghost note
]

# Step 2: Define pitch and time contexts
pitch_context = PitchContext(pitch_source=DIATONIC_MODES["Dorian"], tonicity=True)
time_context = TimeContext(base_note=16)  # Each quantum = 1/16 note

# Step 3: Create the MelodicMotif
motif = MelodicMotif(elements, pitch_context=pitch_context)

# Step 4: Export to pseudocode
pseudocode = motif_to_pseudocode(motif)

# Step 5: Resolve and render
resolver = LilypondResolver(
    pitch_context=pitch_context,
    time_context=time_context,
    reference_midi=62  # D4 as concrete pitch for pitch=0
)

if lilypond_exists:
    print("Rendering motif to PDF...")
    pdf_path = resolver.quick_render(
        pseudocode,
        filename="test_motif_output.ly",
        staff_size=16
    )
    
else:
    print("Skipping LilyPond render: LilyPond binary not found.")
