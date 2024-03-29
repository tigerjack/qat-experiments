from qat.lang.AQASM import X, Z, QRoutine
from oracles.general import Oracle


class FixedStringOracle(Oracle):
    def generate(self, **kwargs) -> QRoutine:
        s = kwargs["s"]
        qrout = QRoutine()
        qreg = qrout.new_wires(self.nqubits)
        for i, c in enumerate(s):
            if c == "0":
                qrout.apply(X, qreg[i])
            elif c != "1":
                raise Exception("only 1 or 0 admissible, found " % c)
        qrout.apply(Z.ctrl(self.nqubits - 1), qreg[:-1], qreg[-1])
        for i, c in enumerate(s):
            if c == "0":
                qrout.apply(X, qreg[i])
        return qrout
