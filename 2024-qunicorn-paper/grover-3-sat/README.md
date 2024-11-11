## 3-SAT Solver with Grover's Algorithm on Qunicorn
This repository demonstrates how to solve a 3-SAT problem using Grover's algorithm. The solution is implemented on Amazon Braket's LocalSimulator and then executed on Qunicorn. The 3-SAT problem is encoded into a quantum circuit, which is then processed and executed remotely using a custom helper function to interact with the Qunicorn platform.


### Quantum Solution with Grover's Algorithm
Grover's algorithm is used to search for the satisfying assignment by leveraging quantum superposition, oracles, and amplitude amplification to enhance the probability of measuring a valid solution.

This script implements Grover’s algorithm for solving the 3-SAT problem by following these steps:

Uniform Superposition: Create an equal superposition of all possible quantum states.
Oracle: Encode the clauses of the 3-SAT problem into a quantum oracle.
Amplitude Amplification: Apply Grover's algorithm to amplify the probability of measuring the solution.
The circuit is then serialized to QASM3 format and executed on the Qunicorn platform.

### Note

The circuit is constructed based on the specific example provided.