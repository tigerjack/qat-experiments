from math import asin, ceil, pi, sqrt
from typing import Tuple

from oracles.general import Oracle
from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.gates import H, X, Z
from qat.lang.AQASM.program import Program
from qat.lang.AQASM.routines import QRoutine

from algorithms.sign_algorithm import SignAlgorithm


class GroverAlgorithm(SignAlgorithm):
    """The property of the given Boolean function is that it is guaranteed to
either be balanced or constant. A constant function returns all 0's or all 1's
for any input, while a balanced function returns 0's for exactly half of all
inputs and 1's for the other half. Our task is to determine whether the given
function is balanced or constant.
    """
    @classmethod
    def generate_program(cls, pr: Program, qr: QRegister,
                         oracle: Oracle) -> Tuple[Program, QRegister]:
        # Add another qubit for output and put it in state \ket{-}
        n = len(qr)
        iters = ceil(pi / (4 * asin(1 / sqrt(2**n))) - 1 / 2)
        if iters == 0:
            iters = 1
        print(f"Grover iters: {iters}")
        qfun_in = cls._input(len(qr))
        pr.apply(qfun_in, qr)
        for _ in range(iters):
            cls._iter(pr, qr, oracle)

        return pr, qr

    @classmethod
    def _iter(cls, pr, qr, oracle):
        qfun_in = cls._input(len(qr))
        qfun_dif = cls._diffusion(len(qr))
        pr.apply(oracle, qr)
        pr.apply(qfun_in.dag(), qr)
        pr.apply(qfun_dif, qr)
        pr.apply(qfun_in, qr)
        return pr, qr

    @classmethod
    def _input(cls, len_input: int) -> QRoutine:
        """Standard input routing"""
        qrout = QRoutine()
        qreg = qrout.new_wires(len_input)
        for qb in qreg:
            qrout.apply(H, qb)
        return qrout

    @classmethod
    def _diffusion(cls, len_diff: int) -> QRoutine:
        qrout = QRoutine()
        qreg = qrout.new_wires(len_diff)
        for qb in qreg:
            qrout.apply(X, qb)
        qrout.apply(Z.ctrl(len_diff - 1), qreg[:-1], qreg[-1])
        for qb in qreg:
            qrout.apply(X, qb)
        return qrout
