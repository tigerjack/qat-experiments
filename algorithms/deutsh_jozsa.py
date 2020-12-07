from qat.lang.AQASM import H, Program, QRegister, X, QRoutine

from oracles.general import Oracle
from algorithms.sign_algorithm import SignAlgorithm

# from qat.core.console import display


class DeutschJozsaAlgorithm(SignAlgorithm):
    @classmethod
    def run(
        cls,
        pr: Program,
        qr: QRegister,
        oracle: QRoutine,
        nqubits: int,
        simulator,
    ):
        # Add another qubit for output and put it in staet \ket{-}
        qout = pr.qalloc(1)
        pr.apply(X, qout)
        pr.apply(H, qout)

        for qb in qr:
            pr.apply(H, qb)
        pr.apply(oracle, [*qr, *qout])
        for qb in qr:
            pr.apply(H, qb)

        res = simulator.submit(pr.to_circ().to_job(qubits=[qr]))
        return res
