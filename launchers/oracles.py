import argparse
import random

from algorithms.bernstein_vazirani import BernsteinVaziraniAlgorithm
from algorithms.deutsch_jozsa import DeutschJozsaAlgorithm
from algorithms.grover import GroverAlgorithm
from qat.core.console import display
from qat.qpus import PyLinalg

from oracles.bernstein_vazirani import BitwiseProductOracle as BPOra
from oracles.deutsch_jozsa import BalancedOracle as BOra
from oracles.deutsch_jozsa import ConstantOracle as COra
from oracles.grover import FixedStringOracle as FSOra


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


def main():
    qpu = PyLinalg()
    namespace = parse_arguments()
    print(namespace)

    if not namespace.bitstring:
        namespace.bitstring = bin(random.getrandbits(namespace.n))[2:].zfill(
            namespace.n)
    print(f"String {namespace.bitstring} ")

    algs_oracles = [
        (DeutschJozsaAlgorithm, COra(namespace.n), {}),
        (DeutschJozsaAlgorithm, BOra(namespace.n), {}),
        (BernsteinVaziraniAlgorithm, BPOra(namespace.n), {
            "s": namespace.bitstring
        }),
        (GroverAlgorithm, FSOra(namespace.n), {
            "s": namespace.bitstring
        }),
    ]

    for alg, oracle, kwargs in algs_oracles:
        print(alg)
        print(oracle)
        print(kwargs)
        oracle_rout = oracle.generate(**kwargs)
        pr, meas_qbits = alg.generate_program(namespace.n, oracle_rout)
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
