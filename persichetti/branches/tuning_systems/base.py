from abc import ABC, abstractmethod

class TuningSystem(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def pitch_frequency(self, pitch_class: int, octave: int = 4) -> float:
        pass

    def tuning_map(self) -> dict:
        raise NotImplementedError