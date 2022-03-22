from copy import deepcopy
from math import pi
from random import random

from qat.lang.AQASM import CNOT, RX, RY, RZ, H, Program, X, Z
from qat.qpus import PyLinalg


def main():
    # _a is for Alice, _b is for Bob, _c is for classical
    pr = Program()
    to_teleport = pr.qalloc()
    epr_pair_a = pr.qalloc()
    epr_pair_a_c = pr.calloc()
    to_teleport_c = pr.calloc()
    epr_pair_b = pr.qalloc()

    # Prepare EPR pair
    pr.apply(H, *epr_pair_a)
    pr.apply(CNOT, *epr_pair_a, *epr_pair_b)
    # Now Alice has her half of the EPR pair (epr_pair_a) and Bob the other one
    # (epr_pair_b qubit)

    # Prepare random state on the qubit(s) to teleport
    pr.apply(RY(random() * pi), *to_teleport)
    pr.apply(RX(random() * pi), *to_teleport)
    pr.apply(RZ(random() * pi), *to_teleport)

    # At this point we make a copy of the original program. The idea is to show
    # the state we would obtain if we would stop at this stage, before the
    # teleportation.
    pr2 = deepcopy(pr)

    # We continue with the teleportation circuit

    # Alice interact her to_teleport_qubit with her half of the EPR pair
    pr.apply(CNOT, *to_teleport, *epr_pair_a)
    pr.apply(H, *to_teleport)
    # ... and then she measures her 2 qubits
    pr.measure(to_teleport, to_teleport_c)
    pr.measure(epr_pair_a, epr_pair_a_c)

    # She then sends her measured qubits to Bob which, depending on their value
    # being 0 or 1, performs the classically controlled X and Z on his own half of the EPR pair
    pr.cc_apply(epr_pair_a_c[0], X, epr_pair_b[0])
    pr.cc_apply(to_teleport_c[0], Z, epr_pair_b[0])

    #
    circ = pr.to_circ()
    circ2 = pr2.to_circ()

    # simulation
    qpu = PyLinalg()
    res = qpu.submit(circ.to_job(qubits=[epr_pair_b]))
    res2 = qpu.submit(circ2.to_job(qubits=[to_teleport]))

    print("Original state, measured on to_teleport qubit")
    for sample in res2:
        # print(f"state {sample.state} with amplitude {sample.amplitude} and probability {sample.probability}")
        print(f"state {sample.state} with amplitude {sample.probability}")
    print("Teleported state, measured on ")
    for sample in res:
        print(f"state {sample.state} with probability {sample.probability}")


if __name__ == '__main__':
    main()
