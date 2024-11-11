import requests
from braket.circuits.serialization import IRType

def execute_on_qunicorn(circuit, origin='http://localhost:8080'):
  '''
    Executes a quantum circuit on a Qunicorn server by submitting the circuit for batch processing, 
    deploying the program, creating a job, and retrieving the results.

    This function interacts with the Qunicorn API, sending requests to deploy the quantum circuit, 
    initiate a job, and retrieve the results of the execution. It assumes the Qunicorn server is 
    running at the specified `origin` (default is 'http://localhost:8080').

    Parameters:
    -----------
    circuit : dict
        The quantum circuit in QASM3/QASM2 format to be executed.
    
    origin : str, optional, default='http://localhost:8080'
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
  
  # put circuits into a deployment for batch execution
  programs = [{"quantumCircuit": circuit, "assemblerLanguage": "QASM3"}]

  payload = {
    "programs": programs,
    "name": "GroverDeployment"
  }

  # Send POST request to create a deployment
  print("Creating Deployment")
  deployment_response = requests.post(f'{origin}/deployments/', json=payload)
  print(deployment_response.url)
  print(deployment_response.status_code)

  #input("Press ENTER to continue...\n")

  if deployment_response.status_code == 201:
    # Extract deployment ID from the response
    content = deployment_response.json()
    deployment_id = content['id']

    # Payload dictionary for creating a job
    payload = { 
      "name": "GroverJob",
      "providerName": "IBM",
      "deviceName": "aer_simulator",
      "shots": 1000,
      "errorMitigation": "none",
      "cutToWidth": "none",
      "token": "",
      "type": "RUNNER",
      "deploymentId": deployment_id 
    }
    
    # Send POST request to create a job
    job_response = requests.post(f'{origin}/jobs/', json=payload)



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
    # Send GET request to retrieve job results
    result = requests.get(f'{origin}/jobs/{job_id}/results/')


  # aggregate result
  if result.status_code == 200:
    # Process the results
    all_counts = []
    for res in result.json():
      if res['resultType'] == 'COUNTS':
        counts = res['data']
        all_counts.append(counts)

  return all_counts
