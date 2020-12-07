import random
import sys
from typing import Tuple

from qat.lang.AQASM import Program, QRegister
from qat.qpus import PyLinalg

from algorithms.bernstein_vazirani import BernsteinVaziraniAlgorithm
from algorithms.deutsh_jozsa import DeutschJozsaAlgorithm
from oracles.bernstein_vazirani import BitwiseProductOracle
from oracles.deutsch_jozsa import BalancedOracle, ConstantOracle


def create_program(nqubits: int) -> Tuple[Program, QRegister]:
    pr = Program()
    qr = pr.qalloc(nqubits)
    return pr, qr


def main():
    # TODO take from input
    qpu = PyLinalg()
    n = int(sys.argv[1])

    s = bin(random.getrandbits(n))[2:].zfill(n)

    algs_oracles = [
        (DeutschJozsaAlgorithm, ConstantOracle(n), {}),
        (DeutschJozsaAlgorithm, BalancedOracle(n), {}),
        (BernsteinVaziraniAlgorithm, BitwiseProductOracle(n), {"s": s}),
    ]

    for alg, oracle, kwargs in algs_oracles:
        print(alg)
        print(oracle)
        print(kwargs)
        pr, qr = create_program(n)
        oracle_rout = oracle.generate(**kwargs)
        ress = alg.run(pr, qr, oracle_rout, n, qpu)
        for res in ress:
            print(res.state, res.probability)
        print("***")


if __name__ == "__main__":
    main()
