# EduScan V2

*A classroom assistant for seamless student identification and academic data retrieval using open-source solutions.*

## Project Description
Eduscan is a python application that uses OpenFaas and AWS services like S3, DynamoDB to process uploaded classroom videos, recognize students' faces and retrieve academic data.

**Key Tasks:**

1. **Video Upload**: Users upload videos to an S3 input bucket.

2. **Video Processing**: OpenFaaS function processes videos, extracts frames, and recognizes faces.

3. **Face Recognition**: Academic data is retrieved based on recognized faces from DynamoDB.

4. **Data Preloading**: Student data is preloaded into DynamoDB.

5. **Custom OpenFaaS Function**: Utilize a custom container image with preinstalled tools.

6. **Custom Kubernetes Cluster**: Deploy OpenFaaS function in a minimal Kubernetes cluster with KinD.

7. **Academic Data Storage**: Store academic info in CSV format in an S3 output bucket.

8. **Testing**: Sample videos and workload generator for testing.

**Deliverables:**

- OpenFaaS and KinD cluster for video processing.
- DynamoDB preloading with academic data.
- Properly formatted content in the output S3 bucket.
- Sample videos for testing.
- Workload generator for validation.

This project aims to enhance classroom management with efficient student recognition and data retrieval.

![OpenFaaS Eduscan Architecture](https://github.com/sreeharsha-rav/openfaas-eduscan/blob/main/openfaas-eduscan.png)

## Installation and Usage

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- AWS account with access to S3, DynamoDB
- Docker with Docker Desktop, Docker Hub
- Git Bash if on Windows
- VS Code

### Usage

1. Clone the repository:
   ```sh
   git clone https://github.com/sreeharsha-rav/openfaas-eduscan.git
   ```

2. Navigate to the project folder:
   ```sh
   cd openfaas-eduscan
   ```

3. Go to the `dynamoDB-setup` folder and use the code to set up DynamoDB.

4. Go to the `openfaas-setup` folder and use the code to set up OpenFaas.

6. Go to the `workload-testing` folder and follow the instructions to test the OpenFaas function.

## Credits

This project is part of CSE 546 - Cloud Computing course curriculum at ASU.