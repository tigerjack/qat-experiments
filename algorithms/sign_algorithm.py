from abc import ABC, abstractclassmethod
from typing import Tuple

from qat.lang.AQASM.program import Program
from qat.lang.AQASM.bits import QRegister
from qat.qpus import CommonQPU
from oracles.general import Oracle


class SignAlgorithm(ABC):

    @abstractclassmethod
    def generate_program(cls, pr: Program, qr: QRegister, oracle: Oracle)-> Tuple[Program, QRegister]:
        """Returns a program and a quantum register to measure
        """
        pass

    @classmethod
    def simulate_program(cls,
                         pr: Program,
                         qpu: CommonQPU,
                         circ_args={},
                         job_args={}):
        cr = pr.to_circ(**circ_args)
        jb = cr.to_job(**job_args)
        res = qpu.submit(jb)
        # print("simulation over")
        return res
