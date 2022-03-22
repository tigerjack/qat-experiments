from typing import Any, Dict, Tuple

from oracles.general import Oracle
from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.program import Program
from algorithms.algorithm import Algorithm
from abc import abstractclassmethod


class SignAlgorithm(Algorithm):
    @abstractclassmethod
    def generate_program(cls, nqbits: int,
                         oracle: Oracle) -> Tuple[Program, QRegister]:
        """Returns a program and a quantum register to measure
        """
        pass
