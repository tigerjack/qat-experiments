from qat.lang.AQASM.gates import H, X
from qat.lang.AQASM.program import Program
from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.routines import QRoutine

from oracles.general import Oracle
from algorithms.sign_algorithm import SignAlgorithm


class DeutschJozsaAlgorithm(SignAlgorithm):
    """The property of the given Boolean function is that it is guaranteed to
either be balanced or constant. A constant function returns all 0's or all 1's
for any input, while a balanced function returns 0's for exactly half of all
inputs and 1's for the other half. Our task is to determine whether the given
function is balanced or constant.
    """

    @classmethod
    def generate_program(cls, nqbits:int, oracle: Oracle):
        # Add another qubit for output and put it in state \ket{-}
        pr = Program()
        qr = pr.qalloc(nqbits)
        qout = pr.qalloc(1)
        pr.apply(X, qout)
        pr.apply(H, qout)

        for qb in qr:
            pr.apply(H, qb)
        pr.apply(oracle, [*qr, *qout])
        for qb in qr:
            pr.apply(H, qb)
        return pr, qr


