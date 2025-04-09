# Persichetti and Python

![CI](https://github.com/joelhumann/persichetti-and-python/actions/workflows/ci.yml/badge.svg)

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://joelhumann.github.io/persichetti-and-python/)

**A composer's operating system based on Vincent Persichetti's _Twentieth-Century Harmony_.**

This is a full-featured Python package for theory, composition, and analysis, structured around Persichetti's classic book, with parallel branches for tuning systems, orchestration, and contemporary practice.

---

## Features

- Logic-based, intervallic model of pitch and scale
- Fully abstract diatonic and modal systems ("bare metal musicology")
- Compositional primitives: motifs, rhythm, meter, texture
- Voice and part handling with local metric frames
- Pedagogical mode tracks Persichetti chapter by chapter
- Extensible to post-tonal and just intonation practice

---

## Project Structure

```
persichetti/
├── fundamentals/       # primitives: pitch, tuning, time, event
├── core/               # chapter-based tools (Persichetti)
├── branches/           # parallel theory tracks (tuning, orchestration)
├── composition/        # general composition tools
├── analysis/           # general analysis tools
├── output/             # rendering, export, audio, midi
├── pedagogy/           # GUI and curriculum helpers
├── utils/              # helpers, logging, converters
├── examples/           # usage demos per chapter/module
```

External:
- `engravers/` (outside root): LilyPond tools (GPL-licensed)

---

## Usage

```bash
pip install -e .
```

Then in Python:
```python
from persichetti.fundamentals import Pitch, Interval
from persichetti.core.scales import DIATONIC_MODES
```

---

## Tests & CI

This repository uses GitHub Actions for continuous integration.

- ✅ Cross-platform: Ubuntu, macOS, Windows
- ✅ Python 3.9 and 3.10
- ✅ Linting via `flake8`
- ✅ Tests via `pytest`

To run tests locally:
```bash
pytest tests/
```

---

## Coming Soon

- Score rendering via Abjad
- Real-time composition GUI
- Curriculum and course builder
- Export to LilyPond, MIDI, SuperCollider

---

## License

Core code is MIT licensed. `engravers/` contains GPL LilyPond tooling and is excluded from builds.

---

## Maintainer

Joel Humann — [humann.co.uk](https://www.humann.co.uk) | [@joelhumann](https://bsky.app/profile/joelhumann.bsky.social)
