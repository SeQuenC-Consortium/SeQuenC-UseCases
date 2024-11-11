import requests
from braket.circuits.serialization import IRType
from time import sleep

def execute_on_qunicorn(circuit, origin='http://localhost:5005'):
  '''
    Executes a quantum circuit on a Qunicorn server by submitting the circuit for batch processing, 
    deploying the program, creating a job, and retrieving the results.

    This function interacts with the Qunicorn API, sending requests to deploy the quantum circuit, 
    initiate a job, and retrieve the results of the execution. It assumes the Qunicorn server is 
    running at the specified `origin` (default is 'http://localhost:5005').

    Parameters:
    -----------
    circuit : dict
        The quantum circuit in QASM3/QASM2 format to be executed.
    
    origin : str, optional, default='http://localhost:5005'
        The URL of the Qunicorn server. This is the endpoint to which requests are sent to deploy and 
        run the quantum circuit.

    Returns:
    --------
    list
        A list of dictionaries containing the execution counts of different measurement outcomes from 
        the quantum circuit execution. Each dictionary in the list represents counts of different 
        possible measurement results.

    Raises:
    -------
    requests.exceptions.RequestException
        If an error occurs during the HTTP requests (e.g., connection error, timeout, or bad response),
        a `requests.exceptions.RequestException` will be raised.
  '''
  
  programs = [{"quantumCircuit": circuit, "assemblerLanguage": "QASM3"}]

  payload = {
    "programs": programs,
    "name": "GroverDeployment"
  }

  # Send POST request to create a deployment
  print("Creating Deployment")
  deployment_response = requests.post(f'{origin}/deployments/', json=payload, verify = False)
  print(deployment_response.url)
  print(deployment_response.status_code)

  #input("Press ENTER to continue...\n")

  if deployment_response.status_code == 201:
    # Extract deployment ID from the response
    content = deployment_response.json()
    deployment_id = content['id']

    # Payload dictionary for creating a job
    # Pauli Twirling was used as error-mitigation method
    payload = { 
      "name": "GroverJob",
      "providerName": "IBM",
      "deviceName": "aer_simulator",
      "shots": 4000,
      "errorMitigation": "pauli_twirling",
      "token": "",
      "type": "RUNNER",
      "deploymentId": deployment_id 
    }
    
    #print("Deploying Job")
    # Send POST request to create a job
    job_response = requests.post(f'{origin}/jobs/', json=payload)
    #print(job_response.url)
    #print(job_response.status_code)

  print(job_response.json())
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

  print(all_counts)
  print("solutions should be '0x5', '0x0', '0x3'")

  return all_counts
