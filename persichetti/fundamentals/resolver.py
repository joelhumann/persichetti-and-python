# fundamentals/resolver.py

from typing import List, Dict, Optional, Union
from fractions import Fraction
from pathlib import Path
import subprocess
import platform
import json

from .pitch_context import PitchContext
from .quantum_time import TimeContext
from .event import Note, Rest

# System-wide output directory relative to project root
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_lilypond_version(lilypond_path: Path) -> str:
    try:
        result = subprocess.run(
            [str(lilypond_path), "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if "GNU LilyPond" in line:
                return line.split()[2]
    except Exception:
        pass
    return "2.24.0"  # fallback

class LilypondResolver:
    def __init__(self, pitch_context: PitchContext, time_context: TimeContext, reference_midi: int = 62):
        self.pitch_context = pitch_context
        self.time_context = time_context
        self.reference_midi = reference_midi
        self.lilypond_path = Path(__file__).resolve().parents[2] / "engravers" / "lilypond" / "bin" / "lilypond"
        self.lilypond_version = get_lilypond_version(self.lilypond_path)

    def determine_clef(self, pseudocode: dict) -> str:
        midi_pitches = [
            self.reference_midi + el["pitch"]
            for el in pseudocode["elements"]
            if el["type"] == "note" and el.get("pitch") is not None
        ]
        if not midi_pitches:
            return "treble"
        avg = sum(midi_pitches) / len(midi_pitches)
        if avg < 50:
            return "bass"
        elif avg > 64:
            return "treble"
        else:
            return "alto"

    def resolve_pitch(self, relative_pitch: int) -> str:
        abs_pitch = self.reference_midi + relative_pitch
        return self.midi_to_lilypond(abs_pitch)

    def midi_to_lilypond(self, midi: int) -> str:
        pitch_names = ['c', 'cis', 'd', 'ees', 'e', 'f', 'fis', 'g', 'gis', 'a', 'bes', 'b']
        pitch_class = midi % 12
        octave = (midi // 12) - 4
        lily_base = pitch_names[pitch_class]
        if octave > 0:
            return lily_base + "'" * octave
        elif octave < 0:
            return lily_base + "," * abs(octave)
        else:
            return lily_base

    def resolve_duration(self, quantum_units: Optional[int]) -> str:
        return self.time_context.quanta_to_lilypond(quantum_units) if quantum_units else ""

    def resolve_element(self, element: Dict[str, Union[str, int, None, bool]]) -> str:
        kind = element["type"]
        pitch = element.get("pitch")
        dur = element.get("duration")
        dur_str = self.resolve_duration(dur)

        if kind == "rest":
            return f"r{dur_str}"
        elif kind == "note":
            return f"{self.resolve_pitch(pitch)}{dur_str}"
        elif kind == "xnote":
            resolved_pitch = self.resolve_pitch(pitch if pitch is not None else 71 - self.reference_midi)
            return f"\\once \\override NoteHead.style = #'cross {resolved_pitch}{dur_str}"
        else:
            raise ValueError(f"Unknown element type: {kind}")

    def resolve_motif(self, pseudocode: Dict) -> str:
        return " ".join(self.resolve_element(elem) for elem in pseudocode["elements"])

    def write_lilypond_file(
        self,
        music_string: str,
        filename: str = "motif_output.ly",
        staff_size: int = 18,
        pseudocode: Optional[dict] = None,
    ) -> Path:
        file_path = OUTPUT_DIR / filename
        lilypond_version = self.lilypond_version
        clef = f"\\clef {self.determine_clef(pseudocode) if pseudocode else 'treble'}"

        lilypond_code = f"""\\version "{lilypond_version}"

\\paper {{
  #(set-paper-size "a4")
  indent = 0\\mm
}}

\\layout {{
  \\context {{
    \\Score
    \\remove "Bar_number_engraver"
  }}
  \\context {{
    \\Staff
    \\override StaffSymbol.staff-space = #{staff_size / 4}
  }}
}}

\\score {{
  \\new Staff {{
    {clef}
    \\relative c' {{
      {music_string}
    }}
  }}
}}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(lilypond_code)

        return file_path

    def compile_pdf(self, filename: str = "motif_output.ly") -> Path:
        file_path = OUTPUT_DIR / filename
        if not file_path.exists():
            raise FileNotFoundError(f"LilyPond file not found: {file_path}")

        system = platform.system()
        engraver_root = Path(__file__).resolve().parents[2] / "engravers" / "lilypond"
        engraver_bin = engraver_root / "bin" / ("lilypond.exe" if system == "Windows" else "lilypond")

        if not engraver_bin.exists():
            raise FileNotFoundError(f"LilyPond binary not found at: {engraver_bin}")

        subprocess.run(
            [str(engraver_bin), "--output", str(OUTPUT_DIR), str(file_path)],
            check=True
        )

        return OUTPUT_DIR / (file_path.stem + ".pdf")
    
    def quick_render(self, pseudocode: dict, filename: str = "motif_output.ly", staff_size: int = 18) -> Path:
        """
        Resolves, writes pseudocode, writes LilyPond, and compiles to PDF.
        """
        # Write pseudocode to .json
        json_out = OUTPUT_DIR / (filename.replace(".ly", "_pseudocode.json"))
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(pseudocode, f, indent=2)
    
        # Continue with rendering
        music_string = self.resolve_motif(pseudocode)
        ly_path = self.write_lilypond_file(music_string, filename, staff_size)
        return self.compile_pdf(ly_path.name)

