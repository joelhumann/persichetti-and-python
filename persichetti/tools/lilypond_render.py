# persichetti/tools/lilypond_render.py

import subprocess
from persichetti.config import LILYPOND_PATH


def compile_lilypond(ly_file_path: str):
    """
    Compile a .ly file using LilyPond.
    Output: .pdf and .midi files in the same directory.
    """
    if LILYPOND_PATH is None:
        raise RuntimeError("LilyPond executable not found. Set LILYPOND_PATH or install it.")

    try:
        subprocess.run([LILYPOND_PATH, ly_file_path], check=True)
        print(f"LilyPond rendered: {ly_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running LilyPond: {e}")
        raise
