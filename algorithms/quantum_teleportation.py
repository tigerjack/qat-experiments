from copy import deepcopy
from math import pi
from random import random

from qat.lang.AQASM import CNOT, RX, RY, RZ, H, Program, X, Z
from qat.qpus import PyLinalg


def main():
    pr = Program()
    nqbits = 1
    to_teleport = pr.qalloc(nqbits)
    epr_pair_a = pr.qalloc()
    epr_pair_a_c = pr.calloc()
    to_teleport_c = pr.calloc(nqbits)
    epr_pair_b = pr.qalloc()

    # prepare EPR pair
    pr.apply(H, *epr_pair_a)
    pr.apply(CNOT, *epr_pair_a, *epr_pair_b)

    # Prepare random state
    pr.apply(RY(random() * pi), *to_teleport)
    pr.apply(RX(random() * pi), *to_teleport)
    pr.apply(RZ(random() * pi), *to_teleport)
    pr2 = deepcopy(pr)

    # teleport
    pr.apply(CNOT, *to_teleport, *epr_pair_a)
    pr.apply(H, *to_teleport)
    pr.measure(to_teleport, to_teleport_c)
    pr.measure(epr_pair_a, epr_pair_a_c)

    # cc
    pr.cc_apply(epr_pair_a_c[0], X, epr_pair_b[0])
    pr.cc_apply(to_teleport_c[0], Z, epr_pair_b[0])

    # final
    circ = pr.to_circ()
    circ2 = pr2.to_circ()

    # simulation
    qpu = PyLinalg()
    res = qpu.submit(circ.to_job(qubits=[epr_pair_b]))
    res2 = qpu.submit(circ2.to_job(qubits=[0]))

    print("Original state to teleport")
    for sample in res2:
        print(sample)
    print("Teleported state")
    for sample in res:
        print(sample)


if __name__ == '__main__':
    main()
