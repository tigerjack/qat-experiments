from abc import ABC, abstractclassmethod

from qat.lang.AQASM import Program, QRegister

from oracles.general import Oracle


class SignAlgorithm(ABC):
    @abstractclassmethod
    def run(
        pr: Program,
        qr: QRegister,
        oracle: Oracle,
        nqubits: int,
        simulator,
    ):
        pass
