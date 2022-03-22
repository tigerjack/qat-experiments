from abc import ABC, abstractclassmethod
from typing import Any, Dict, Tuple

from qat.lang.AQASM.program import Program
from qat.lang.AQASM.bits import QRegister
from qat.qpus import CommonQPU


class Algorithm(ABC):
    @abstractclassmethod
    def generate_program(cls, nqbits: int) -> Tuple[Program, QRegister]:
        """Returns a program and a quantum register to measure
        """
        pass

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
