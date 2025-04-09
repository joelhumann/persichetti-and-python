import pytest
from persichetti.fundamentals.pitch_context import PitchContext
from persichetti.core.scales import DIATONIC_MODES, Scale

def test_pitch_context_rotates_tonic_to_zero():
    mode = DIATONIC_MODES["Dorian"]  # tonic = 2
    context = PitchContext(mode, tonicity=True)
    # Pitch class set should be {0, 2, 3, 5, 7, 9, 10} after rotation
    assert context.is_allowed(0)
    assert context.is_allowed(3)
    assert not context.is_allowed(1)
    assert context.get_reference() == 0
    print("DIATONIC_MODES['Dorian'] tonic:", mode.tonic)
    print("DIATONIC_MODES['Dorian'] base scale:", mode.scale.pitch_classes)
    print("Rotated pitch classes:", mode.absolute_pitch_classes())

def test_pitch_context_absolute_scale():
    scale = Scale("Custom", [0, 2, 4, 7])
    context = PitchContext(scale, tonicity=False, reference_pitch=100)
    assert context.is_allowed(100)
    assert not context.is_allowed(102)

def test_pitch_context_requires_reference_for_tonicity_false():
    scale = Scale("Sparse", [1, 3, 6])
    context = PitchContext(scale, tonicity=False)
    with pytest.raises(ValueError):
        context.get_reference()
    assert context.get_reference(first_pitch=20) == 20
