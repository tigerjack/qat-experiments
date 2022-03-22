from math import pi
from random import random

from qat.lang.AQASM import CNOT, RX, RY, RZ, H, Program, X, Z

from algorithms.algorithm import Algorithm


class TeleportationAlgorithm(Algorithm):
    """This is the full circuit for teleportation. Although it's correct, it's not
    useful on its own since we cannot know the state Alice had before
    measuring. In other words, we do not have any clue on if the teleportation
    worked.

    """
    @classmethod
    def generate_program(cls, nqbits: int):
        pr = Program()
        # TODO extend to nqbits
        nqbits = 1
        to_teleport = pr.qalloc(nqbits)
        to_teleport_c = pr.calloc(nqbits)
        epr_pair_a = pr.qalloc()
        epr_pair_a_c = pr.calloc()
        epr_pair_b = pr.qalloc()

        # Prepare EPR pair
        pr.apply(H, *epr_pair_a)
        pr.apply(CNOT, *epr_pair_a, *epr_pair_b)

        # Prepare random state using 3 random rotation around the 3 axis
        pr.apply(RY(random() * pi), *to_teleport)
        pr.apply(RX(random() * pi), *to_teleport)
        pr.apply(RZ(random() * pi), *to_teleport)

        # Encode
        pr.apply(CNOT, *to_teleport, *epr_pair_a)
        pr.apply(H, *to_teleport)

        # Teleport
        pr.measure(to_teleport, to_teleport_c)
        pr.measure(epr_pair_a, epr_pair_a_c)

        # Decode
        pr.cc_apply(epr_pair_a_c[0], X, epr_pair_b[0])
        pr.cc_apply(to_teleport_c[0], Z, epr_pair_b[0])

        return pr, None
