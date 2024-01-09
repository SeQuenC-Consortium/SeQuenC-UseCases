# Quantum Workflows, MODULO, and QuantME Use Cases

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This project contains different use cases for the SeQuenC-platform.
The main purpose is to show how the different components used in the SeQuenC-project interact with the unification-layer.

More tools used for the use-cases are the following:

- [Quantum Workflow Modeler](https://github.com/SeQuenC-Consortium/workflow-modeler): A graphical BPMN modeler.
- [Camunda BPMN Engine](https://camunda.com/products/camunda-platform/bpmn-engine/): A state-of-the-art BPMN workflow engine used to execute quantum workflows.

### Example 2023

### Qunicorn 2023 - Use-cases

### Consortial 2023 - Stuttgart

### Workshop 2023 - Berlin

## Learn More

- Georg, Daniel; Barzen, Johanna; Beisel, Martin; Leymann, Frank; Obst, Julian; Vietz, Daniel; Weder, Benjamin; Yussupov, Vladimir: [**Execution Patterns for Quantum Applications**](https://www.iaas.uni-stuttgart.de/publications/Georg2023_PatternsQuantumExecution.pdf). In: Proceedings of the 18th International Conference on Software Technologies - ICSOFT, SciTePress, 2023.

- Bühler, Fabian; Barzen, Johanna; Beisel, Martin; Georg, Daniel; Leymann, Frank; Wild, Karoline: [**Patterns for Quantum Software Development**](https://www.iaas.uni-stuttgart.de/publications/Buehler2023_PatternsQuantumSE.pdf). In: Proceedings of the 15th International Conference on Pervasive Patterns and Applications (PATTERNS 2023), Xpert Publishing Services (XPS), 2023.

### Repository structure

```
SEQUENC-USECASES
│   README.md
│
└───USE-CASE
│   │   README.md
│   │
│   └───docker
│   |   │   dockerfile
│   |   |   docker-compose
|   |
│   └───resources
│   |   │   example.jpg
|   |
│   └───workflows
│       │   workflow.bpmn
│       │
```

This structure is the base structure for use-cases.
Important files are the README explaining the use-case in more detail. The docker files used to execute. In the resources folder screenshots, videos or other material can be placed. Another folder, in most examples workflows are in the rspective folder.

## Disclaimer of Warranty

Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.
You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

## Haftungsausschluss

Dies ist ein Forschungsprototyp.
Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden, ausgeschlossen.
