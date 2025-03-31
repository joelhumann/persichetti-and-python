# render.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import argparse
import shutil
from pathlib import Path
from persichetti.config import LILYPOND_PATH
from persichetti.config import LILYPOND_PATH
print("LilyPond path:", LILYPOND_PATH)
from persichetti.tools.lilypond_render import compile_lilypond

# TEMP: dummy motif structure for testing
class FakeMotif:
    def __init__(self):
        # semitone values, C = 0
        self.pitches = [0, 2, 4, 5, 7, None, 7, 5, 4, 2, 0]
        self.durations = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  # all quarter notes

def motif_to_lilypond(motif: FakeMotif) -> str:
    note_names = ["c", "cis", "d", "ees", "e", "f", "fis", "g", "aes", "a", "bes", "b"]
    notes = []

    for pitch, dur in zip(motif.pitches, motif.durations):
        if pitch is None:
            notes.append(f"r{dur}")  # rest
        else:
            pc = pitch % 12
            notes.append(f"{note_names[pc]}{dur}")

    return r"""
\version "2.24.0"
\score {
  \new Staff {
    \relative c' {
      """ + " ".join(notes) + r"""
    }
  }
  \layout { }
  \midi { }
}
"""

def copy_license(output_dir: Path):
    license_src = Path(__file__).resolve().parent / "licenses" / "COPYING.LILYPOND"
    shutil.copy(license_src, output_dir / "COPYING.LILYPOND")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render motif to LilyPond.")
    parser.add_argument("--output", "-o", type=str, default="output/scores")
    args = parser.parse_args()

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    motif = FakeMotif()
    ly_code = motif_to_lilypond(motif)

    ly_path = output_dir / "motif.ly"
    ly_path.write_text(ly_code)
    compile_lilypond(str(ly_path))

    copy_license(output_dir)
    print(f"Rendered: {ly_path} → PDF and MIDI\nLicense included.")
