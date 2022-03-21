from qat.lang.AQASM.program import Program
from oracles.general import Oracle
from algorithms.sign_algorithm import SignAlgorithm
from math import pi, ceil, sqrt
from qat.lang.AQASM.gates import H, X
from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.program import Program

class GroverAlgorithm(SignAlgorithm):
    """The property of the given Boolean function is that it is guaranteed to
either be balanced or constant. A constant function returns all 0's or all 1's
for any input, while a balanced function returns 0's for exactly half of all
inputs and 1's for the other half. Our task is to determine whether the given
function is balanced or constant.
    """

    @classmethod
    def generate_program(cls, pr: Program, qr: QRegister, oracle: Oracle):
        # Add another qubit for output and put it in state \ket{-}
        qout = pr.qalloc(1)
        n = len(qr)
        iter = ceil(pi/4 * sqrt(2**n))
        print(iter)
        for _ in range(iter):
            cls._iter(pr, qr, qout, oracle)
        for qb in qr:
            pr.apply(H, qb)
        return pr, qr


    @classmethod
    def _iter(cls, pr, qr, qout, oracle):
        pr.apply(X, qout)
        pr.apply(H, qout)

        for qb in qr:
            pr.apply(H, qb)
        pr.apply(oracle, [*qr, *qout])
        for qb in qr:
            pr.apply(H, qb)

        for qb in qr:
            pr.apply(X, qb)
        pr.apply(X.ctrl(len(qr)), qr, qout)
        for qb in qr:
            pr.apply(X, qb)

        pr.apply(X, qout)
        pr.apply(H, qout)

        return pr, qr
