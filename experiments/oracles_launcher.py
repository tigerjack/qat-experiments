import random
# import sys
from typing import Tuple

from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.program import Program
from qat.qpus import PyLinalg

from algorithms.bernstein_vazirani import BernsteinVaziraniAlgorithm
from algorithms.deutsch_jozsa import DeutschJozsaAlgorithm
from algorithms.grover_algorithm import GroverAlgorithm
from oracles.bernstein_vazirani import BitwiseProductOracle
from oracles.deutsch_jozsa import BalancedOracle, ConstantOracle
from oracles.grover import FixedStringOracle

from qat.core.console import display

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        "Launch one experiment")
    parser.add_argument(
        "-n",
        type=int,
        default=1,
        help="n of qubits")
    parser.add_argument("--display", action="store_true")
    namespace = parser.parse_args()

    return namespace


def create_program(nqubits: int) -> Tuple[Program, QRegister]:
    pr = Program()
    qr = pr.qalloc(nqubits)
    return pr, qr


def main():
    # TODO Grover
    qpu = PyLinalg()
    namespace = parse_arguments()
    print(namespace)
    n = namespace.n


    s = bin(random.getrandbits(n))[2:].zfill(n)
    print(f"Random string {s} ")

    algs_oracles = [
        (DeutschJozsaAlgorithm, ConstantOracle(n), {}),
        (DeutschJozsaAlgorithm, BalancedOracle(n), {}),
        (BernsteinVaziraniAlgorithm, BitwiseProductOracle(n), {"s": s}),
        (GroverAlgorithm, FixedStringOracle(n), {"s": s}),
    ]

    for alg, oracle, kwargs in algs_oracles:
        print(alg)
        print(oracle)
        print(kwargs)
        pr, qr = create_program(n)
        oracle_rout = oracle.generate(**kwargs)
        pr, meas_qbits = alg.generate_program(pr, qr, oracle_rout)
        cr = pr.to_circ()
        display(cr, max_depth=10)
        ress = alg.simulate_program(pr, qpu, job_args={'qubits': meas_qbits})
        for res in ress:
            print(res.state, res.probability)
        print("***")


if __name__ == "__main__":
    main()
