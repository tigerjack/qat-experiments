from algorithms.oracles.general import Oracle
from qat.lang.AQASM import QRoutine, X


class ConstantOracle(Oracle):
    def generate(self, **kwargs):
        qrout = QRoutine()
        # + 1 for the output
        _ = qrout.new_wires(self.nqubits)
        qout = qrout.new_wires(1)
        if kwargs['output'] == 1:
            qrout.apply(X, qout)
        return qrout


class BalancedOracle(Oracle):
    pass
