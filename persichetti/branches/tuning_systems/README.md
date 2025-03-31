# Tuning Systems (Branch: tuning_systems)

This branch provides a historically grounded and extensible framework for modeling musical tuning systems in Python.

## Structure

Each tuning system is encapsulated in its own module and inherits from a common `TuningSystem` interface. Historical coverage is based on J. Murray Barbour's *Tuning and Temperament: A Historical Survey*, with room for modern and digital adaptations.

### Implemented

- `PythagoreanTuning` — Classical Greek and Medieval systems
- `JustIntonationZarlino` — Renaissance-era pure intervals
- `EqualTemperament` — Modern 12-tone equal temperament

### Utilities

- Cent and ratio converters in `historical_utils.py`
- MIDI/frequency converters in `digital_contexts.py`

### Planned

- Meantone and Well Temperament modules
- Golden Ratio tuning and adaptive models
- Integration with psychoacoustic and digital systems

## Usage

Import any system and compute pitch frequencies:

```python
from just_intonation import JustIntonationZarlino
ji = JustIntonationZarlino()
freq = ji.pitch_frequency(4, 4)  # E4 in just intonation
```

## Documentation

Historical notes and system summaries are stored in `docs/barbour_notes.md`.