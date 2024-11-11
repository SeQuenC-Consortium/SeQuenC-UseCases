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

'''
Due to incompatibilites in QASM3 features, we define the czz as custom gate instead of operator
Therefore we replaced the unitary definition with the defined gates
'''
custom_gate_czz = '''\ninclude \"stdgates.inc\";\ngate mcphase (p_0) q_0, q_1 {\ncp(pi/2) q_0, q_1;\n}\ngate ccz q_0, q_1, q_2 {\ncx q_0, q_2;\nU(0, -pi/8, -pi/8) q_2;\ncx q_1, q_2;\nU(0, -7*pi/8, -7*pi/8)q_2;\ncx q_0, q_2;\nU(0, -pi/8, -pi/8) q_2;\ncx q_1, q_2;\nU(0, -7*pi/8, -7*pi/8) q_2;\nmcphase(pi/2) q_0, q_1;\n}\n'''

# This leads to the valid json string
# Remark: To be json compatible, we inserted \n and escaped characters
resulting_qasm3_string = '''
OPENQASM 3.0;\ninclude \"stdgates.inc\";\ngate mcphase (p_0) q_0, q_1 {\ncp(pi/2) q_0, q_1;\n}\ngate ccz q_0, q_1, q_2 {\ncx q_0, q_2;\nU(0, -pi/8, -pi/8) q_2;\ncx q_1, q_2;\nU(0, -7*pi/8, -7*pi/8)q_2;\ncx q_0, q_2;\nU(0, -pi/8, -pi/8) q_2;\ncx q_1, q_2;\nU(0, -7*pi/8, -7*pi/8) q_2;\nmcphase(pi/2) q_0, q_1;\n}\nbit[3] b;\nqubit[3] q;\nh q[0];\nh q[1];\nh q[2];\ncz q[0], q[1];\nz q[2];\nx q[0];\nz q[0];\nx q[0];\nx q[0];\nx q[2];\nccz q[0], q[2], q[1];\nx q[0];\nx q[2];\nh q[0];\nx q[0];\nh q[1];\nx q[1];\nh q[2];\nx q[2];\nh q[2];\nccx q[0], q[1], q[2];\nh q[2];\nx q[0];\nh q[0];\nx q[1];\nh q[1];\nx q[2];\nh q[2];\nb[0] = measure q[0];\nb[1] = measure q[1];\nb[2] = measure q[2];
'''

execute_on_qunicorn(resulting_qasm3_string)