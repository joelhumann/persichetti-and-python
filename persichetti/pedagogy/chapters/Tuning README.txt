# Persichetti Tuning Demo

This is a minimal modular example demonstrating how to build compositional tools in Python using pluggable tuning systems.

It provides:
- A `TuningSystem` abstract interface
- Two implementations: `EqualTemperament` and `JustIntonation`
- A `Pitch` class that computes frequency based on pitch class, octave, and tuning
- An `Interval` class that calculates semitone distance and frequency ratios
- A runnable `main.py` demo showing how these classes work

## File Overview

- `tuning.py` – Defines the `TuningSystem` interface, `EqualTemperament`, and `JustIntonation` systems.
- `pitch.py` – Defines the `Pitch` class which calculates frequencies using a tuning system.
- `interval.py` – Defines the `Interval` class with semitone and frequency ratio methods.
- `main.py` – Example script comparing C and E in both tuning systems.

## Requirements

- Python 3.7+
- No external libraries required

## Running the Demo

```bash
python main.py
