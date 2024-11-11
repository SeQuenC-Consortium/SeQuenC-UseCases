import numpy as np
from time import sleep
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.circuit import Parameter
from qiskit.opflow import I, X, Y, Z
from qiskit.compiler import transpile
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

import requests

# ~~~~~~~~~~~~~~~~~~~ QAOA ~~~~~~~~~~~~~~~~~~~ # 
def operator_from_graph(G: Graph) -> str:
  operator = 0
  for u, v in G.edges():
    s = ['I']*len(G)  # List ['I', 'I', ..], as many Is as nodes
    s[u] = 'Z'
    s[v] = 'Z'
    s = s[::-1]  # reverse, so qbit 0 is node 0
    weight = G[u][v]['weight'] if 'weight' in G[u][v] else 1  # case for weighted graph
    operator += eval('^'.join(s)) * weight
  return -0.5 * operator


def qaoa_circuit(G: Graph):
  # Problem instance
  operator = operator_from_graph(G)

  # Parameter
  gamma = Parameter(r'gamma')
  beta = Parameter(r'beta')

  qaoa = QAOA(reps=1)
  qaoa_qc = qaoa.construct_circuit([beta, gamma], operator)[0]
  qaoa_qc.measure_all()

  #qaoa_qc = transpile(qaoa_qc, basis_gates=['h', 'ry', 'rz', 'rx', 'cx'])
  qaoa_qc = transpile(qaoa_qc, basis_gates=['h', 'ry', 'rzz', 'rx', 'rz'])

  print(qaoa_qc)
  return qaoa_qc


def cut_value(G: Graph, x) -> int:
  #val = cutValueDict.get(x)
  #if val is not None:
  #  return val
  result = 0
  if isinstance(x, str):
    # reverse the string since qbit 0 is LSB
    x = x[::-1]  
  for edge in G.edges():
    u, v = edge
    #weight = G.get_edge_data(u,v, 'weight')['weight']
    if x[u] != x[v]: 
      result += 1 #weight
  #cutValueDict[x] = result
  return result

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 


def execute_on_qunicorn(circuit, origin='http://localhost:8080'):
  # put circuits into a deployment for batch execution
  programs = [{"quantumCircuit": circuit.qasm(), "assemblerLanguage": "QASM2"}]

  payload = {
    "programs": programs,
    "name": "QAOADeployment"
  }

  # Send POST request to create a deployment
  #print("Creating Deployment")
  deployment_response = requests.post(f'{origin}/deployments/', json=payload)
  #print(deployment_response.url)
  #print(deployment_response.status_code)

  #input("Press ENTER to continue...\n")

  if deployment_response.status_code == 201:
    # Extract deployment ID from the response
    content = deployment_response.json()
    deployment_id = content['id']

    # Payload dictionary for creating a job
    payload = { 
      "name": "QAOA_Cutting_Job",
      "providerName": "IBM",
      "deviceName": "aer_simulator",
      "errorMitigation": "none",
      "cutToWidth": 3,
      "shots": 1000,
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
  print(job_id)
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
  # x = beta, gamma
  final_meas_circuits = param_circuit.assign_parameters(x)
  #final_meas_circuits = [c.assign_parameters(x) for c in param_circuit]
  # execute circuits
  result_counts = execute_on_qunicorn(final_meas_circuits)[0]

  #calculate energy
  energy = 0
  for cut, prob in result_counts.items():
    # TODO convert to bin with num_qubits digits
    cut = bin(int(cut, 16))[2:].zfill(len(G)) # convert hex to bin
    energy += cut_value(G, cut) * prob  #energy of whole graph
  # find out how many shots were executed in total
  sum_shots = sum([v for _,v in result_counts.items()]) 
  energy = energy / sum_shots

  print("QAOA energy", energy)
  return -energy


# create QAOA example
G = Graph(nodetype=int)
G.add_edges_from([(0,1),(1,2),(1,3),(2,3),(3,4),(4,0)])
param_circuit = qaoa_circuit(G)

np.random.seed(42)
initial_param_values = np.random.rand(len(param_circuit.parameters))*2*np.pi

res = minimize(objective, initial_param_values, method="COBYLA", options={"maxiter": 200})   
print(res)

#nx.draw(G, with_labels=True)
#plt.show()
