from qat.lang.AQASM import X, QRoutine
from oracles.general import Oracle


class FixedStringOracle(Oracle):
    def generate(self, **kwargs) -> QRoutine:
        s = kwargs["s"]
        qrout = QRoutine()
        qreg = qrout.new_wires(self.nqubits)
        qout = qrout.new_wires(1)
        for i, c in enumerate(s):
            if c == "0":
                qrout.apply(X, qreg[i])
            elif c != "1":
                raise Exception("only 1 or 0 admissible, found " % c)
        qrout.apply(X.ctrl(self.nqubits), qreg, qout)
        for i, c in enumerate(s):
            if c == "0":
                qrout.apply(X, qreg[i])
        return qrout
