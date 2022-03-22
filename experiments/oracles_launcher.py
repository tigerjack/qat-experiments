import argparse
import random
# import sys
from typing import Tuple

from algorithms.bernstein_vazirani import BernsteinVaziraniAlgorithm
from algorithms.deutsch_jozsa import DeutschJozsaAlgorithm
from algorithms.grover_algorithm import GroverAlgorithm
from oracles.bernstein_vazirani import BitwiseProductOracle
from oracles.deutsch_jozsa import BalancedOracle, ConstantOracle
from oracles.grover import FixedStringOracle
from qat.core.console import display
from qat.lang.AQASM.bits import QRegister
from qat.lang.AQASM.program import Program
from qat.qpus import PyLinalg


def parse_arguments():
    parser = argparse.ArgumentParser("Launch one experiment")
    parser.add_argument("-n", type=int, default=1, help="n of qubits")
    parser.add_argument(
        "--bitstring",
        type=str,
        help=
        ("bitstring used by Bernstein-Vazirani and Grover. If not given, it's chosen at random"
         ))
    parser.add_argument("--display",
                        action="store_true",
                        help="If true, display circuit")
    namespace = parser.parse_args()

    return namespace


def create_program(nqubits: int) -> Tuple[Program, QRegister]:
    pr = Program()
    qr = pr.qalloc(nqubits)
    return pr, qr


def main():
    qpu = PyLinalg()
    namespace = parse_arguments()
    print(namespace)
    n = namespace.n

    if namespace.bitstring == None:
        s = bin(random.getrandbits(n))[2:].zfill(n)
    else:
        s = namespace.bitstring
    print(f"Random string {s} ")

    algs_oracles = [
        (DeutschJozsaAlgorithm, ConstantOracle(n), {}),
        (DeutschJozsaAlgorithm, BalancedOracle(n), {}),
        (BernsteinVaziraniAlgorithm, BitwiseProductOracle(n), {
            "s": s
        }),
        (GroverAlgorithm, FixedStringOracle(n), {
            "s": s
        }),
    ]

    for alg, oracle, kwargs in algs_oracles:
        print(alg)
        print(oracle)
        print(kwargs)
        pr, qr = create_program(n)
        oracle_rout = oracle.generate(**kwargs)
        pr, meas_qbits = alg.generate_program(pr, qr, oracle_rout)
        cr = pr.to_circ()
        if namespace.display:
            display(cr)
        # High amp_threshold, but it's fine for our oracles
        ress = alg.simulate_program(pr,
                                    qpu,
                                    job_args={
                                        'qubits': meas_qbits,
                                        'amp_threshold': 1e-1
                                    })
        for res in ress:
            print(res.state, res.probability)
        print("***")


if __name__ == "__main__":
    main()
