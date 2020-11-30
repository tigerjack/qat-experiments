from typing import Tuple

from qat.lang.AQASM import H, Program, QRegister
from qat.qpus import PyLinalg

from algorithms.oracles.deutsch_jozsa_oracles import (BalancedOracle,
                                                      ConstantOracle)
from algorithms.oracles.general import Oracle


def create_program(nqubits: int) -> Tuple[Program, QRegister]:
    pr = Program()
    qr = pr.qalloc(nqubits)
    return pr, qr


def run(oracle: Oracle, nqubits: int, simulator):
    pr, qr = create_program(nqubits)
    qout = pr.qalloc(1)
    for qb in qr:
        pr.apply(H, qb)
    pr.apply(oracle.generate(output=0), [*qr, *qout])
    for qb in qr:
        pr.apply(H, qb)

    res = simulator.submit(pr.to_circ().to_job())
    return res


def main():
    # TODO take from input
    qpu = PyLinalg()
    n = 4
    oracle = ConstantOracle(n)
    ress = run(oracle, n, qpu)
    for res in ress:
        print(res.state, res.probability)

    # TODO
    oracle = BalancedOracle(n)


if __name__ == "__main__":
    main()