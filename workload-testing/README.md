# README for Workload Testing

This Python script is used to manage and run workloads on AWS S3 buckets. It provides functionalities to clear input and output buckets, upload files to these buckets, and run workload generators.

## Scripts

- `workload.py`: This script generates workload for AWS S3 buckets.
- `trigger-setup.py`: This script set's up trigger functionatily to invoke OpenFaas function.

## Usage
To run and test workload, follow these steps:

1. **Setup trigger first in one terminal:**
    ```
    python trigger-setup.py
    ```
2. **Start workload in another terminal:**
    ```
    python workload.py
    ```

## Requirements
- AWS S3 buckets for input and output, provide bucket names in `workload.py`.
- AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) must be set in the `config.py` file.
- OpenFaaS function URL is to be provided in `trigger-setup.py`.
- Test case directories containing .mp4 files for testing.
- Setup DynamoDB given in `dynamoDB-setup` folder.
- Setup OpenFaas given in `openfaas-setup` folder.

## Note
This script uses the boto3 AWS SDK for Python to interact with AWS S3 and DynamoDB. Make sure to install it using pip:

```bash
pip install boto3
```