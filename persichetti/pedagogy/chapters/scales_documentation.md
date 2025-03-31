# `scales.py` Module Documentation

This module is part of a developing codebase inspired by Vincent Persichetti’s *Twentieth-Century Harmony*. It provides a foundational toolkit for defining and transforming modal systems, with an extensible architecture that will later incorporate intervals, chords, and full harmonic pathfinding.

---

## 🧠 Conceptual Framework

### Modal System
A `ModalSystem` is defined by:
- A **tonic** (pitch class from 0–11)
- A **scale** (a set of relative pitch classes, e.g. `[0, 2, 4, 5, 7, 9, 11]` for diatonic)
- An optional **alias** list (e.g. “Lydian Dominant” = “Overtone”)
- An optional `as_mode_of` field to identify its parent **scale type** (e.g. “Diatonic”, “Melodic Minor”)

Each modal system supports:
- Mapping scale degrees to absolute pitch classes
- Mapping absolute pitch classes back to degrees
- Retrieving the absolute pitch class set

---

## 🔧 Core Classes & Functions

### `ModalSystem`
```python
ModalSystem(tonic: int, scale: Scale, aliases: Optional[List[str]] = None, as_mode_of: Optional[str] = None)
```
A representation of a mode as it functions in context — distinguished by its tonic.

### `group_modal_systems_by_scale_type(...)`
Groups modal systems into families according to their `as_mode_of` field.

---

## 🔁 ModalTransformer Class
A transformation engine for working with modal systems.

### Features:
- Modal Interchange: Change mode, keep tonic
- Modal Modulation: Change tonic, keep mode
- Full Modal Transformation: Change one or both
- Undo / Redo
- Branching: Create parallel paths of transformation
- Shared Tone Analysis
- Tonal Pathfinding: Discover transformation paths between modal systems

### `modal_interchange()`
```python
def modal_interchange(source: ModalSystem, target_mode_name: str) -> Optional[ModalSystem]
```
Changes the mode while retaining the tonic.

### `modal_modulation()`
```python
def modal_modulation(source: ModalSystem, new_tonic: int) -> ModalSystem
```
Changes the tonic while retaining the mode and scale type.

### `full_modal_transformation()`
```python
def full_modal_transformation(source, new_mode_name=None, new_tonic=None)
```
Allows for mode and/or tonic change in a single step.

### `shared_tones()`
Returns the pitch classes in common between two modal systems.

### `print_history()`
Prints the logged transformation history with tonic, scale type, and transformation type.

### `undo_last_transformation()` / `redo_last_transformation()`
Traverse the transformation log backward or forward.

### `branch()` / `switch_branch()`
Creates a new alternative path from the current transformation state and allows switching between different transformation branches.

### `find_paths()`
```python
def find_paths(start, goal, max_depth=3, match_threshold=4, allow_modulation=True)
```
A recursive pathfinding function to find modal paths with sufficient shared tones.

### `apply_chain()`
Executes a list of transformation steps programmatically.

---

## ⚠️ Scaffolded Features (Pending)
The following are conceptually integrated but not yet implemented:

### ✅ Chord Hierarchies (Persichetti)
We will associate triadic chord hierarchies to each `ModalSystem` based on:
- **Primary chords**
- **Auxiliary chords**
- **Color chords**

Diatonic modes will have these hierarchies **explicitly encoded**. For other modes, we will **derive chord hierarchies algorithmically** using heuristics from Persichetti, to be detailed in a future session.

### 🔄 Migrating Objects Beyond Pitches
Modal transformations will be generalized to operate on:
- **Intervals** (`IntervalPathfinder`)
- **Chords** (`ChordPathfinder`) — where chords are simultaneities

This will allow transformation chains in which intervals or chords migrate from one modal system to another.

---

## 🔜 Next Steps
- Define `Simultaneity` (chord) class
- Annotate and extract triadic chord hierarchies per modal system
- Implement interval and chordal pathfinding
- Extend `ModalTransformer` to support migrating intervals and chords
- Generate transformation diagrams or visualizations

---

## 🔗 Theoretical Basis
This toolkit draws directly from the pedagogical structure of *Twentieth-Century Harmony* by Vincent Persichetti. Its goal is to support:
- Modal writing and interchange
- Polymodal and synthetic scale systems
- Algorithmic composition based on interval and harmonic logic

Further theoretical alignment with Persichetti’s approach will occur chapter by chapter.

