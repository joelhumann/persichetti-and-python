import pytest
from persichetti.fundamentals.event import Note, Rest
from persichetti.fundamentals.melodic_motif import MelodicMotif
from persichetti.fundamentals.pitch_context import PitchContext
from persichetti.core.scales import DIATONIC_MODES

@pytest.fixture
def dorian_pitch_context():
    # DIATONIC_MODES["Dorian"] has tonic=2, becomes pitch 0 in context
    return PitchContext(DIATONIC_MODES["Dorian"], tonicity=True)

def test_rhythmic_motif_in_dorian_context(dorian_pitch_context):
    # Valid pitch values according to rotated Dorian: [0, 2, 3, 5, 7, 9, 10]
    elements = [
        Note(1, 0),  # Tonic
        Note(1, 2),  # +2 semitones
        Note(1, 3),  # +3 semitones
        Rest(1),
        Note(1, 5),  # +5 semitones
    ]
    motif = MelodicMotif(elements, pitch_context=dorian_pitch_context)
    assert motif.is_rhythmic()
    assert motif.total_duration == 5
    assert motif.get_pitches() == [0, 2, 3, None, 5]

def test_free_motif_without_context():
    # No pitch context: normalize relative to first pitched note
    elements = [
        Note(None, pitch=12),
        Note(None, pitch=14),
        Rest(None),
        Note(None, pitch=15),
    ]
    motif = MelodicMotif(elements)
    assert motif.is_free()
    assert motif.total_duration is None
    assert motif.get_pitches() == [0, 2, None, 3]

def test_pitch_not_allowed_raises(dorian_pitch_context):
    elements = [
        Note(1, 0),   # valid
        Note(1, 1),   # 1 % 12 not in rotated Dorian
    ]
    with pytest.raises(ValueError):
        MelodicMotif(elements, pitch_context=dorian_pitch_context)

def test_mixed_durations_raises():
    elements = [
        Note(1, 0),
        Note(None, 2),
    ]
    with pytest.raises(ValueError):
        MelodicMotif(elements)

def test_copy_preserves_structure(dorian_pitch_context):
    elements = [Note(1, 0), Rest(1)]
    motif = MelodicMotif(elements, pitch_context=dorian_pitch_context)
    clone = motif.copy()
    assert motif.get_pitches() == clone.get_pitches()
    assert motif.total_duration == clone.total_duration
    assert motif.elements is not clone.elements
    assert all(e1 is not e2 for e1, e2 in zip(motif.elements, clone.elements))
