from typing import List


class Metre:
    """
    Represents a metrical structure for a rhythmic motif.

    A Metre object defines how time is *grouped* within a rhythmic structure
    using integer groupings (measured in quantum units) and specifies how
    the motif aligns — or fails to align — with that structure.

    ----
    GROUPINGS:
    - A list of integers, each representing the duration (in quanta) of a metrical group.
    - Groupings model perceptual units like beats or subdivisions.
    - Each grouping must typically be ≥ 2, with exceptions allowed for anacrusis or overhang
      depending on the alignment mode (see below).

    ----
    ALIGNMENT:
    Specifies how the motif is metrically aligned at its start and end:

    • "closed":
        Motif begins at the start of the first group and ends precisely at the end of the last group.
        → All groupings must be ≥ 2.

    • "anacrusis":
        Motif begins *inside* the first group (e.g., with a pickup) but ends at the end of the last group.
        → First group may be ≥ 1; remaining groups must be ≥ 2.

    • "overhang":
        Motif begins aligned, but ends *within* the last group (e.g., with a cadential tail).
        → Final group may be ≥ 1; earlier groups must be ≥ 2.

    • "open":
        Motif begins and ends *within* groups.
        → First and last groups may be ≥ 1; internal groups must be ≥ 2.

    ----
    EXAMPLES:
        Metre([4, 4, 4], alignment="closed")
        Metre([1, 4, 3], alignment="anacrusis")
        Metre([4, 4, 1], alignment="overhang")
        Metre([1, 3, 2, 1], alignment="open")
    """

    def __init__(self, groupings: List[int], alignment: str = "closed"):
        valid_alignments = ("closed", "anacrusis", "overhang", "open")

        if alignment not in valid_alignments:
            raise ValueError(f"Alignment must be one of {valid_alignments}.")

        if not groupings or not all(isinstance(g, int) and g > 0 for g in groupings):
            raise ValueError("All metrical groups must be positive integers.")

        self.groupings = groupings
        self.alignment = alignment
        self._validate_groupings()

    def _validate_groupings(self):
        g = self.groupings
        a = self.alignment

        if a == "closed":
            if not all(x >= 2 for x in g):
                raise ValueError("All groupings must be ≥ 2 for 'closed' alignment.")

        elif a == "anacrusis":
            if g[0] < 1:
                raise ValueError("First group (anacrusis) must be ≥ 1.")
            if not all(x >= 2 for x in g[1:]):
                raise ValueError("All groups after the anacrusis must be ≥ 2.")

        elif a == "overhang":
            if not all(x >= 2 for x in g[:-1]):
                raise ValueError("All groups except the final must be ≥ 2.")
            if g[-1] < 1:
                raise ValueError("Final group (overhang) must be ≥ 1.")

        elif a == "open":
            if g[0] < 1 or g[-1] < 1:
                raise ValueError("First and last groups must be ≥ 1.")
            if not all(x >= 2 for x in g[1:-1]):
                raise ValueError("All internal groups must be ≥ 2.")

    def total_duration(self) -> int:
        """Returns the total metrical span in quantum units."""
        return sum(self.groupings)

    def is_regular(self) -> bool:
        """Returns True if all groupings are the same length."""
        return len(set(self.groupings)) == 1

    def group_count(self) -> int:
        """Returns the number of metrical groups."""
        return len(self.groupings)

    def anacrusis_length(self) -> int:
        """
        Returns the duration (in quanta) of the anacrusis if applicable.
        For 'anacrusis' or 'open' alignments, returns the first group.
        Returns 0 otherwise.
        """
        if self.alignment in ("anacrusis", "open"):
            return self.groupings[0]
        return 0

    def overhang_length(self) -> int:
        """
        Returns the duration (in quanta) of the overhang if applicable.
        For 'overhang' or 'open' alignments, returns the final group.
        Returns 0 otherwise.
        """
        if self.alignment in ("overhang", "open"):
            return self.groupings[-1]
        return 0

    def __repr__(self) -> str:
        """Returns a human-readable string representation."""
        group_str = "+".join(str(g) for g in self.groupings)
        return f"Metre({group_str}, alignment='{self.alignment}')"

    def as_tuple(self) -> tuple:
        """Returns a hashable tuple representation."""
        return (tuple(self.groupings), self.alignment)

    def to_dict(self) -> dict:
        """Returns a JSON-serializable representation."""
        return {
            "groupings": self.groupings,
            "alignment": self.alignment,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Metre":
        """Reconstructs a Metre object from a dictionary."""
        return cls(groupings=data["groupings"], alignment=data["alignment"])
