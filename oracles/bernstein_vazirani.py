from qat.lang.AQASM import CNOT, QRoutine

from oracles.general import Oracle


class BitwiseProductOracle(Oracle):
    def generate(self, **kwargs):
        s = kwargs["s"]
        qrout = QRoutine()
        qreg = qrout.new_wires(self.nqubits)
        qout = qrout.new_wires(1)
        for i, c in enumerate(s):
            if c == "1":
                qrout.apply(CNOT, qreg[i], qout)
            elif c != "0":
                raise Exception("only 1 or 0 admissible")
        return qrout
