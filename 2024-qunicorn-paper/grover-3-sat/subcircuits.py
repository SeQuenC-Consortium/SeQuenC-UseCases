import operator

from braket.circuits import Circuit, circuit
from braket.devices import LocalSimulator
from math import pi
import numpy as np


## Implement the ccz-gate

# Helper function to build C-C-Z gate
@circuit.subroutine(register=True)
def ccz(targets=[0, 1, 2]):
    """
    implementation of three-qubit gate CCZ
     **Not compatible with IBM**
    """
    # define three-qubit CCZ gate
    ccz_gate = np.array(
        [
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        ],
        dtype=complex,
    )

    # instantiate circuit object
    circ = Circuit()

    # add CCZ gate
    circ.unitary(matrix=ccz_gate, targets=targets)

    return circ



# Helper function to build a uniform superposition
@circuit.subroutine(register=True)
def uniform_superposition(num_qubits):
    """
    implementation of a uniform superposition
    """

    # instantiate circuit object
    circ = Circuit()

    # add CCZ gate
    for i in range(num_qubits):
        circ.h(i)

    return circ


# Helper function to build a uniform superposition
@circuit.subroutine(register=True)
def oracle():
    """
    implementation of the grover oracle
    """

    # instantiate circuit object
    circ = Circuit()

    # build the circuit for the instance
    circ.cz(0,1).z(2).x(0).z(0).x(0).ccz([0,2,1])

    return circ


# Helper function to build a uniform superposition
@circuit.subroutine(register=True)
def amplitude_amplification():
    """
    implementation of the amplitude amplification
    """

    # instantiate circuit object
    circ = Circuit()
    for _ in range(3):
        circ.h(_)
        circ.x(_)
    circ.h(2)
    circ.ccnot(0,1,2)
    circ.h(2)
    for _ in range(3):
        circ.x(_)
        circ.h(_)

    return circ

