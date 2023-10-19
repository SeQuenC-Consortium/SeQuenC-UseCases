# SeQuenC-UseCases


## Setup: 

1. Run qunicorn, camunda and the workflow modeller using the provided docker-compose
2. The services should now be available under:
   1. qunicorn: localhost:5005/swagger-ui/
   2. workflowmodeller: localhost:8080/
   3. camunda: localhost:8078/camunda/app/

## Running the Use Cases

1. Have Qunicorn, Camunda and the Workflowmodeller running (possibly using the docker-compose).
2. Open the Workflowmodeller.
3. Configure the Workflowmodeller, so it uses the correct Camunda Endpoint.
4. Open the Use Case to be executed.
5. Deploy the Use Case.
6. Open Camunda, navigate to Camunda Tasklist.

   ![CamundaOverview](./resources/camunda_overview_app.JPG)
8. Click "Start process" on the top right.

   ![TaskListOverview](./resources/camunda_task_list_overview.JPG)
10. The Deployed Workflow should appear here.
11. Click on the Workflow and configure the Inputs if necessary.

   ![InitialInput](./resources/initial_input_example.JPG)
12. Start the process.
13. UserTasks will appear in the Tasklist.

   ![UserTaskInList](./resources/user_task_example.JPG)
14. Click on the UserTask and evaluate it. 
   
   ![UserTaskDetails](./resources/user_task_detail_example.JPG)

## Description of the Use Cases

### Get Devices and Create Job:
1. Get all devices
2. UserTask: Let the user evaluate the results, the user can now select a device
3. Create a job with the choosen device, and other user inputs
4. Get the results/details of the job
5. UserTask: Let the user evaluate the results

![UseCase1](./resources/use_case_1_bpmn.JPG)

### Rerun Job: (Aer_simulator, QISKIT, IBM)
1. Rerun a job
2. Get the results/details of the job
3. UserTask: Let the user evaluate the resuls

![UseCase2](./resources/use_case_2_bpmn.JPG)

### Get a Provider List
1. Get all providers
2. UserTask: Let the user evaluate the results 

![UseCase3](./resources/use_case_3_bpmn.JPG)

### Create and Delete a Deployment
1. Create a deployment
2. Get the deployment details, and get deployment X
3. UserTask: Evaluate Results of the deployment details
4. Delete the deployment
5. Get all deployment
6. UserTask: Evaluate results and check if the deployment X is missing again

![UseCase4](./resources/use_case_4_bpmn.JPG)

### Create, Run and Delete BRAKET Job on AWS
1. Create a job for AWS using Braket
2. Get the results/details of the job
3. UserTask: Let the user evaluate the results
4. Delete the job
5. Get all Jobs
6. UserTask: Let the user check if the job got deleted and is not in the list anymore

![UseCase5](./resources/use_case_5_bpmn.JPG)

### Create, Run BRAKET Deployment on IBM
1. Create a job for IBM using Braket
2. Get the results/details of the job
3. UserTask: Let the user evaluate the results

![UseCase6](./resources/use_case_6_bpmn.JPG)

### Create QRISP Deployment and run on IBM
1. Create a deployment using QRISP
2. Create a job using the created deployment
3. Get the results/details of the job
4. UserTask: Let the user evaluate the results

![UseCase7](./resources/use_case_7_bpmn.JPG)

### Create Deployment with User Inputs and then a Job with UserInputs:
1. Create a deployment using defined User Inputs
2. Get the details of the deployment
3. UserTask: Let the User evaluate the deployment
4. Create a job
5. Get the results/details of the job
6. UserTask: Let the user evaluate the results

![UseCase8](./resources/use_case_8_bpmn.JPG)

## Naming Scheme for new Use Cases

Use_Case_#NR_Description
