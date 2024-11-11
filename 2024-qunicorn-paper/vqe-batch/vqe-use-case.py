import numpy as np
from time import sleep
from scipy.optimize import minimize
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit.opflow.primitive_ops import PauliSumOp
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


# circuits are hardcoded

def create_circuits():
  problem_size = int(np.log2(len(operator_matrix)))
  ans = EfficientSU2(num_qubits=problem_size, reps=2)
  circuits = [ans.copy() for i in range(3)]
  
  # Add Y measurement
  circuits[0].sdg(0)
  circuits[0].h(0)
  # Add X measurement
  circuits[0].h(1)
  # ZZ needs no additional

  # Add IX/ZX measurement
  circuits[2].h(1)

  # Add measurement
  for c in circuits:
    c.measure_all()

  return circuits
  

def execute_on_qunicorn(circuits, origin='http://localhost:8080'):
  # put circuits into a deployment for batch execution
  programs = [{"quantumCircuit": c.qasm(), "assemblerLanguage": "QASM2"} for c in circuits]

  payload = {
    "programs": programs,
    "name": "VQEDeployment"
  }

  # Send POST request to create a deployment
  #print("Creating Deployment")
  deployment_response = requests.post(f'{origin}/deployments/', json=payload)
  #print(deployment_response.url)
  #print(deployment_response.status_code)

#  input("Press ENTER to continue...\n")

  if deployment_response.status_code == 201:
    # Extract deployment ID from the response
    content = deployment_response.json()
    deployment_id = content['id']

    # Payload dictionary for creating a job
    payload = { 
      "name": "VQE_Batch_Job",
      "providerName": "IBM",
      "deviceName": "aer_simulator",
      "shots": 1000,
      "errorMitigation": "none",
      "token": "",
      "type": "RUNNER",
      "deploymentId": deployment_id 
    }
    
    #print("Deploying Job")
    # Send POST request to create a job
    job_response = requests.post(f'{origin}/jobs/', json=payload)
    #print(job_response.url)
    #print(job_response.status_code)


  # get info of job
  job_id = job_response.json()['id'] 
  job_state = job_response.json()['state'] 

  while job_state in ["READY", "RUNNING"]:
    sleep(0.05)
    job_state = requests.get(f'{origin}/jobs/{job_id}').json()['state']



  if job_response.status_code == 201:
    # Extract job ID from the response
    content = job_response.json()
    job_id = content['id']
    #print("Requesting Results")
    # Send GET request to retrieve job results
    result = requests.get(f'{origin}/jobs/{job_id}/results/')
    #print(result.url)
    #print(result.status_code)

  # aggregate result
  if result.status_code == 200:
    # Process the results
    all_counts = []
    for res in result.json():
      if res['resultType'] == 'COUNTS':
        counts = res['data']
        all_counts.append(counts)

  return all_counts


def objective(x):
  final_meas_circuits = [c.assign_parameters(x) for c in param_circuits]
  # execute circuits
  result_counts = execute_on_qunicorn(final_meas_circuits)

  exp = 0.0
  for i in range(len(pauli_lists)):
      paulis = pauli_lists[i]
      counts = result_counts[i]

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
  return exp.real


# create VQE example
param_circuits = create_circuits()

np.random.seed(42)
initial_param_values = np.random.rand(len(param_circuits[0].parameters))*2*np.pi

res = minimize(objective, initial_param_values, method="COBYLA", options={"maxiter": 200})   
print(res)
