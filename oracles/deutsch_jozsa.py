from qat.lang.AQASM.gates import CNOT, X
from qat.lang.AQASM.routines import QRoutine

from oracles.general import Oracle


class ConstantOracle(Oracle):

    def generate(self, **kwargs):
        qrout = QRoutine()
        # + 1 for the output
        _ = qrout.new_wires(self.nqubits)
        qout = qrout.new_wires(1)
        if "output" in kwargs and kwargs["output"] == 1:
            qrout.apply(X, qout)
        return qrout


class BalancedOracle(Oracle):

    def generate(self, **kwargs):
        qrout = QRoutine()
        # + 1 for the output
        qreg = qrout.new_wires(self.nqubits)
        qout = qrout.new_wires(1)
        for qb in qreg:
            qrout.apply(CNOT, qb, qout)
        return qrout
