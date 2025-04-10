#fundamentals/event.py

from typing import Optional, Union
from fractions import Fraction


class Element:
    """
    Base class for any musical time element (note or rest).

    Duration is expressed as:
    - an integer (e.g., 1, 2)
    - a Fraction (e.g., 2/3, 3/5)
    - or None (for indefinite/free durations)

    Durations must be strictly > 0 if defined.
    """

    def __init__(self, duration: Optional[Union[int, Fraction]]):
        if duration is not None:
            if not isinstance(duration, (int, Fraction)):
                raise TypeError("Duration must be an int, Fraction, or None.")
            if duration <= 0:
                raise ValueError("Duration must be > 0 if defined.")
        self.duration = duration

    def is_note(self) -> bool:
        return isinstance(self, Note)

    def is_rest(self) -> bool:
        return isinstance(self, Rest)

    def is_pitched(self) -> bool:
        return False  # overridden by Note

    def is_unpitched(self) -> bool:
        return not self.is_pitched()

    def kind(self) -> str:
        if self.is_rest():
            return "rest"
        elif self.is_note() and self.is_unpitched():
            return "unpitched_note"
        elif self.is_note():
            return "pitched_note"
        return "unknown"

    def copy(self):
        raise NotImplementedError("Must be implemented in subclass.")

    def scale_duration(self, factor: Union[int, Fraction]):
        if self.duration is None:
            raise ValueError("Cannot scale an indefinite duration.")
        raise NotImplementedError("Must be implemented in subclass.")


class Note(Element):
    def __init__(self, duration: Optional[Union[int, Fraction]], pitch: Optional[int] = None):
        super().__init__(duration)
        self.pitch = pitch  # None = unpitched

    def is_pitched(self) -> bool:
        return self.pitch is not None

    def copy(self):
        return Note(self.duration, self.pitch)

    def scale_duration(self, factor: Union[int, Fraction]):
        if self.duration is None:
            raise ValueError("Cannot scale an indefinite duration.")
        return Note(self.duration * factor, self.pitch)


class Rest(Element):
    def copy(self):
        return Rest(self.duration)

    def scale_duration(self, factor: Union[int, Fraction]):
        if self.duration is None:
            raise ValueError("Cannot scale an indefinite duration.")
        return Rest(self.duration * factor)
