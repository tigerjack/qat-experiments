import unittest

# from qat.core.console import display
from qat.external.utils.qroutines.qregs_init import initialize_qureg_given_int
from qat.lang.AQASM import Program
from qat.qpus import PyLinalg

from oracles.deutsch_jozsa_oracles import BalancedOracle


class OracleDeutschJozsaTest(unittest.TestCase):
    qpu = PyLinalg()

    def test_balanced(self):
        max_qubit = 6
        for n in range(1, max_qubit + 1):
            with self.subTest(n=n):
                # It also creates an additional qubit for output
                oracle = BalancedOracle(n)

                count1 = 0
                for i in range(2 ** n):
                    pr = Program()
                    qreg = pr.qalloc(n)
                    qout = pr.qalloc(1)

                    qr_init = initialize_qureg_given_int(i, qreg, False)
                    pr.apply(qr_init, qreg)
                    pr.apply(oracle.generate(), [*qreg, *qout])
                    # display(pr.to_circ())

                    # res = self.qpu.submit(pr.to_circ().to_job())
                    # for sample in res:
                    #     print(sample.state, sample.probability)

                    res = self.qpu.submit(pr.to_circ().to_job(qubits=[qout]))
                    self.assertEqual(len(res.raw_data), 1)
                    sample = res.raw_data[0]
                    if sample.state.state == 1:
                        count1 += 1

                self.assertEqual(count1, 2 ** (n - 1))
