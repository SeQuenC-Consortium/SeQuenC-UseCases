import numpy as np
from scipy.optimize import minimize
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import SparsePauliOp
from qiskit.opflow.primitive_ops import PauliSumOp
from qiskit.algorithms import VQE
from qiskit import QuantumCircuit

import requests

# define problem instance
seed = 1
np.random.seed(seed)
operator_matrix = np.matrix([[3.+0.j, 2.+0.j, 0.+0.j, 0.-2.5j], 
                             [2.+0.j, -3.+0.j, 0.+2.5j, 0.+0.j], 
                             [0.+0.j, 0.-2.5j, -3.+0.j, 0.+0.j], 
                             [0.+2.5j, 0.+0.j, 0.+0.j, 3.+0.j]])
pauli_operator = SparsePauliOp.from_operator(operator_matrix)
# pauli_lists contains the respective pauli operators that can be estimated from the measument outcomes of each circuit
pauli_lists = pauli_operator.paulis.group_commuting(qubit_wise=True)
#print(pauli_lists)


# create VQE example
problem_size = int(np.log2(len(operator_matrix)))
ans = EfficientSU2(num_qubits=problem_size, reps=2)


# decompose the algorithm into the circuits that are executed
init = np.random.rand(len(ans.parameters))*2*np.pi
circ1 = ans.assign_parameters(init)
circ2 = ans.assign_parameters(init)
circ3 = ans.assign_parameters(init)

# Add Y measurement
circ1.sdg(0)
circ1.h(0)
# Add X measurement
circ1.h(1)

# ZZ needs no additional

# Add IX/ZX measurement
circ3.h(1)

circ1.measure_all()
circ2.measure_all()
circ3.measure_all()

# Base URL for the API endpoint
origin = 'http://localhost:8080'

# Initialize deployment ID (will be set later if successful)
deployment_id = None

# put circuits into a deployment for batch execution
payload = {
  "programs": [
    {
      "quantumCircuit": circ1.qasm(),
      "assemblerLanguage": "QASM2"
    },
    {
      "quantumCircuit": circ2.qasm(),
      "assemblerLanguage": "QASM2"
    },
    {
      "quantumCircuit": circ3.qasm(),
      "assemblerLanguage": "QASM2"
    }
  ],
  "name": "VQEDeployment"
}

print("Creating Deployment")
# Send POST request to create a deployment
deployment_response = requests.post(f'{origin}/deployments/', json=payload)
print(deployment_response.url)
print(deployment_response.status_code)

input("Press ENTER to continue...\n")

if deployment_response.status_code == 201:
  # Extract deployment ID from the response
  content = deployment_response.json()
  deployment_id = content['id']

  # Payload dictionary for creating a job
  payload = { 
    "name": "TestJob",
    "providerName": "IBM",
    "deviceName": "aer_simulator",
    "shots": 1000,
    "token": "",
    "type": "RUNNER",
    "deploymentId": deployment_id 
  }
  
  print("Deploying Job")
  # Send POST request to create a job
  job_response = requests.post(f'{origin}/jobs/', json=payload)
  print(job_response.url)
  print(job_response.status_code)

input("Press ENTER to continue...\n")

if job_response.status_code == 201:
  # Extract job ID from the response
  content = job_response.json()
  job_id = content['id']
  print("Requesting Results")
  # Send GET request to retrieve job results
  result = requests.get(f'{origin}/jobs/{job_id}/results/')
  print(result.url)
  print(result.status_code)
  input("Press ENTER to continue...\n")

### Postprocessing ###

# aggregate result
if result.status_code == 200:
  # Process the results
  all_counts = []
  for res in result.json():
    if res['resultType'] == 'COUNTS':
      counts = res['data']
      all_counts.append(counts)
      print(counts)

  exp = 0.0
  print(len(pauli_lists))
  for i in range(len(pauli_lists)):
      paulis = pauli_lists[i]
      counts = all_counts[i]

      # compute contribution of each pauli operator (p_exp)
      for pauli in paulis:
          p_exp = 0.0
          sum_shots = sum([v for _,v in counts.items()]) # find out how many shots were executed in total
          for k,v in counts.items():
              k = bin(int(k, 16))[2:] # convert hex to bin
              k_pruned = [b for j, b in enumerate(k) if str(pauli)[j] != 'I'] # remove bits where operator is I
              p_exp += (-1)**(k_pruned.count('1')) * v/sum_shots

          # add to overall expectation weighted by coefficient for respective pauli operator
          idx = pauli_operator.paulis.settings["data"].index(str(pauli))
          exp += pauli_operator.coeffs[idx] * p_exp

  print("VQE expectation", exp.real)

