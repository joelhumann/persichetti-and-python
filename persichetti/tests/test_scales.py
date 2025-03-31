from core.scales import Scale, ModalSystem, DIATONIC_MODES


def test_scale_properties():
    s = Scale("MyScale", [0, 2, 4, 7, 9])
    assert s.cardinality == 5
    assert s.category == "pentatonic"
    assert not s.symmetric


def test_modal_system_degree_conversions():
    mode = DIATONIC_MODES["Ionian"]
    assert mode.degree_to_pc(0) == 0
    assert mode.degree_to_pc(1) == 2
    assert mode.pc_to_degree(4) == 2
    assert mode.pc_to_degree(6) is None


def test_modal_system_absolute_pitch_classes():
    mode = DIATONIC_MODES["Mixolydian"]
    pcs = mode.absolute_pitch_classes()
    print("Mixolydian tonic:", mode.tonic)
    print("Mixolydian pitch classes:", pcs)
    assert 6 in pcs
