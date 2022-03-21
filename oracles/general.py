from abc import ABC, abstractmethod

from qat.lang.AQASM.routines import QRoutine


class Oracle(ABC):

    def __init__(self, nqubits: int):
        self.nqubits = nqubits

    @abstractmethod
    def generate(self, **kwargs) -> QRoutine:
        pass
