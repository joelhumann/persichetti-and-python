# Chapter X: Title Goes Here

## A. Theory

### 1. Interval Type and Qualia
Every interval between two equal-tempered pitches has an interval type determined solely by the number of semitones. This type is abstracted from tonal or modal spelling and maps to an interval qualia, which represents the textural or perceptual character of the interval. Most interval types have a fixed qualia, but the perfect fourth and tritone are initialized as 'indeterminate' and require musical context to resolve.  
**Pedagogical Implication:** ⟶ _Describe how this informs compositional thinking._

```python
# Example code demonstrating how interval types map to qualia
interval = Interval(6)  # Tritone
print(interval.qualia)  # TexturalClass('indeterminate')
context = {'environment': 'chromatic'}
print(interval.resolve(context))  # 'neutral'
```

### 2. Representing Interval Objects
An `Interval` object should encapsulate:
- `distance` (int): the number of semitones between two pitch classes (e.g. 3, 15, etc.)
- `type` (str): a named identifier for the interval, based on mod-12 value (e.g. 'min3', 'P4', 'tritone')
- `qualia` (TexturalClass): the sonic character or textural quality, either fixed or 'indeterminate'

Special cases (P4 and tritone) initialize as 'indeterminate' and are resolved with contextual data passed as a dictionary.

```python
# Example construction
from intervals import Interval

interval = Interval(5)  # Perfect fourth
print(interval.type)    # 'P4'
print(interval.qualia)  # TexturalClass('indeterminate')

context = {'environment': 'consonant'}
print(interval.resolve(context))  # 'dissonant'
```

This allows the interval object to defer judgment on ambiguous intervals until enough contextual information is available.

### 3. Intervallic Tension Ranking
- `distance` is the absolute number of semitones between two pitches and may be any non-negative integer.
- `type` is the pitch-class representation of that distance, calculated mod 12 (e.g., 15 semitones → type 'min3').
- `spelling` refers to the notated or theoretical representation (e.g., an interval type of 'min3' might be spelled as an 'aug2' in a given key).
- `qualia` is the textural or perceptual character (e.g., 'soft consonance', 'sharp dissonance').

Persichetti also provides an implicit ranking of intervallic tension in diatonic contexts, from least to most tense. This ranking can be implemented using a dictionary and referenced as needed.

```python
# Persichetti's intervallic tension in diatonic context
DIATONIC_TENSION_RANK = {
    "oct": 1, "P5": 2, "P4": 3, "maj3": 4, "min6": 5, "min3": 6,
    "maj6": 7, "min7": 8, "maj2": 9, "maj7": 10, "min2": 11, "tritone": 12
}

# Suggested chromatic ordering (reflecting tritone as 'neutral' and P4 as dissonant):
CHROMATIC_TENSION_RANK = {
    "oct": 1, "P5": 2, "maj3": 3, "min3": 4, "maj6": 5, "min6": 6,
    "tritone": 7, "maj2": 8, "min7": 9, "P4": 10, "maj7": 11, "min2": 12
}

# In the Interval class:
@property
def tension_rank(self, context=None):
    if context and context.get("environment") == "chromatic":
        return CHROMATIC_TENSION_RANK.get(self.type)
    return DIATONIC_TENSION_RANK.get(self.type)
```

This ranking helps analyze or generate passages with a controlled tension profile.

### Affective Modifiers for Intervals Above the Octave
Persichetti notes that intervals greater than an octave take on expressive character distinct from their base type. These changes can be modeled using an optional `affective_modifier()` method, which returns a qualitative descriptor of how an interval's qualia shifts with register:

```python
def affective_modifier(self):
    if self.distance < 12:
        return "normal"
    elif self.qualia.label in {"soft consonance", "open consonance"}:
        return "richer"
    elif self.qualia.label in {"sharp dissonance", "mild dissonance"}:
        return "brilliant"
    elif self.qualia.label == "restless":
        return "less restless"  # Persichetti notes it becomes calmer at large intervals
    elif self.qualia.label == "neutral":
        return "veiled"
    return "extended"
```

This modifier can be used analytically or compositionally to inform register-sensitive choices in texture and voice-leading.

### Custom Tension Rankings
Because intervallic tension is mutable and context-sensitive, the system allows users to override the default rankings. For example, a composer working in an experimental idiom might define a different hierarchy of interval tension:

```python
custom_rank = {
    "tritone": 1, "min2": 2, "maj7": 3, "maj2": 4,
    "min7": 5, "P4": 6, "min6": 7, "maj6": 8,
    "min3": 9, "maj3": 10, "P5": 11, "oct": 12
}
interval = Interval(6)
print(interval.tension_rank(custom_rank=custom_rank))
```

This allows for creative and stylistic flexibility in how intervals are understood and deployed. Spelling is still ignored at this stage but may become relevant in tonal/modal modules later.

---

## B. Applications (Toolsets and Methods)

### Application Group 1: (e.g., Two-part writing in two-voice work)
- Description: _What musical/compositional task is being addressed?_
- Tools involved: [e.g., Interval, PitchClass, Qualia analysis]
- Methods: _How the tools are applied or combined to solve the problem._

### Application Group 2: (...)
(Repeat)

---

## C. Compositional Prompts (Persichetti's "Applications")

### Prompt 1:
> Write a short passage featuring primarily mild dissonance and contextual perfect fourths.

🛠 Suggested tools:
- `Interval.qualia`
- `Interval.resolve(context)`
- Future: `KeyCenter` for spelling / modulation

🎯 Strategy:
Describe how to approach this task with code.

```python
# Sketch / macro for generating or analyzing a solution
```

(Repeat for other prompts)
