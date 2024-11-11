import operator

from braket.circuits import Circuit, circuit
from braket.devices import LocalSimulator
from math import pi
import numpy as np
# import matplotlib.pyplot as plt
from subcircuits import uniform_superposition, oracle, amplitude_amplification
from braket.circuits.serialization import IRType
from braket.ir.openqasm import Program
from qunicorn_helper import execute_on_qunicorn

'''
Problem definition of the 3-SAT
DIMACS-CNF format
No custom method for encoding, therefore the circuit is build manually
'''
problem_definition = '''
c example DIMACS-CNF 3-SAT
p cnf 3 5
-1 -2 -3 0
1 -2 3 0
1 2 -3 0
1 -2 -3 0
-1 2 3 0
'''

num_qubits = 3

# Initialize the Braket circuit
grover_circuit = Circuit()

grover_circuit.uniform_superposition(num_qubits).oracle().amplitude_amplification()
qasm_ir = grover_circuit.to_ir(IRType.OPENQASM)

# Find the index of the first and last single quote
start_index = str(qasm_ir).find("OPENQASM")
end_index = str(qasm_ir).rfind(";")

# Slice the string from the first to the last single quote
circuit_string = str(qasm_ir)[start_index:end_index+1]

execute_on_qunicorn(circuit_string)