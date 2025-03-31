import pytest
from fundamentals.event import Note, Rest


def test_note_pitched_and_copy():
    n = Note(2, pitch=60)
    assert n.duration == 2
    assert n.pitch == 60
    assert n.is_note()
    assert not n.is_rest()
    assert n.is_pitched()
    c = n.copy()
    assert c.duration == 2 and c.pitch == 60
    assert c is not n


def test_unpitched_note_behavior():
    n = Note(1, pitch=None)
    assert not n.is_pitched()
    assert n.is_unpitched()


def test_rest_behavior():
    r = Rest(1)
    assert r.duration == 1
    assert r.is_rest()
    assert not r.is_note()
    assert not r.is_pitched()
    assert r.kind() == "rest"


def test_scale_duration_note_and_rest():
    n = Note(2, pitch=62)
    n_scaled = n.scale_duration(2)
    assert n_scaled.duration == 4 and n_scaled.pitch == 62

    r = Rest(2)
    r_scaled = r.scale_duration(3)
    assert r_scaled.duration == 6
