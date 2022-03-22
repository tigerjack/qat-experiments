from abc import ABC, abstractclassmethod
from typing import Any, Dict, Tuple

from oracles.general import Oracle
from qat.core.qpu.qpu import CommonQPU
from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.program import Program


class SignAlgorithm(ABC):
    @abstractclassmethod
    def generate_program(cls, pr: Program, qr: QRegister,
                         oracle: Oracle) -> Tuple[Program, QRegister]:
        """Returns a program and a quantum register to measure
        """

    @classmethod
    def simulate_program(cls,
                         pr: Program,
                         qpu: CommonQPU,
                         circ_args: Dict[str, Any] = {},
                         job_args: Dict[str, Any] = {}):
        cr = pr.to_circ(**circ_args)
        jb = cr.to_job(**job_args)
        res = qpu.submit(jb)
        return res
