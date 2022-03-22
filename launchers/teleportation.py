import argparse
from qat.lang.AQASM import CNOT, RX, RY, RZ, H, Program, X, Z
from qat.qpus import PyLinalg
from qat.core.console import display
from qat.core.magic.magic import QAT
from algorithms.teleportation import TeleportationAlgorithm

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
    alg = TeleportationAlgorithm
    pr, meas_qbits = alg.generate_program(namespace.n)
    ress = alg.simulate_program(pr,
                                qpu)
    for res in ress:
        print(res.state, res.probability)
    print("***")






if __name__ == '__main__':
    main()
