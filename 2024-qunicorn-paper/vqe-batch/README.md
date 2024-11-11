# VQE use case for qunicorn
### Setup (exemplary for Ubuntu and Python 3.11): 
- ``git clone https://github.com/SeQuenC-Consortium/SeQuenC-UseCases.git``
- ``cd SeQuenC-UseCases/2024-qunicorn-paper/vqe-batch``
- ``sudo -H pip install virtualenv`` (if you don't have virtualenv installed)
- ``virtualenv venv`` (create virtualenv named 'venv')
- ``source venv/bin/activate`` (enter virtualenv; in Windows systems activate might be in ``venv/Scripts``)
- ``pip install -r requirements.txt`` (install application requirements)

### Usage:
- Start Qunicorn via docker: ``docker compose up -d``

Qunicorn will be running at ``http://localhost:8080``
- Execute the VQE use case: ``py vqe-use-case.py``


### Disclaimer of Warranty

Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.
