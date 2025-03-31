import os
import platform
import shutil
from pathlib import Path
from typing import Optional


def find_lilypond_path() -> Optional[str]:
    """
    Attempts to find the LilyPond executable.
    Priority:
    1. Environment variable (LILYPOND_PATH)
    2. Bundled binary in project /engravers/lilypond/bin/
    3. System PATH (via shutil.which)
    """
    # 1. Environment override
    env_path = os.environ.get("LILYPOND_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    # 2. Platform-specific binary name
    binary_name = "lilypond.exe" if platform.system() == "Windows" else "lilypond"

    # 3. Look in bundled engravers/lilypond/bin/
    project_root = Path(__file__).resolve().parent.parent
    bundled = project_root / "engravers" / "lilypond" / "bin" / binary_name
    if bundled.exists():
        return str(bundled)

    # 4. Fallback to system PATH
    system_path = shutil.which(binary_name)
    if system_path:
        return system_path

    # Not found
    return None


LILYPOND_PATH = find_lilypond_path()


