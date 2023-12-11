# README for OpenFaas function setup

## Description
This folder contains the source code for an OpenFaaS function named `eduscan-handler`.

The script `handler.py` contains calls the function `face_recognition_handler`, which handles the face recognition process. It downloads a video file from an S3 bucket, processes it to recognize a face, retrieves academic information from DynamoDB based on the recognized face, writes the results to a CSV file, and uploads the output file to another S3 bucket.

## Requirements
- Python 3.8 or above
- An AWS account with two S3 buckets already set up, including bucket names.
- An AWS account with a DynamoDB table already set up, including the table name and partition key.
- An AWS account with Elastic Container Registry (ECR) access.
- AWS credentials (Access Key ID and Secret Access Key).
- Have `arkade` installed, with git bash.
- You have `faas-cli` installed and configured in your terminal.
- You have `helm` installed in your terminal.
- You have `kubectl` installed with `arkade`.
- You have `docker` installed and configured, along with `docker-desktop`, `docker-hub` and you are logged in to your docker account on the terminal. 
- Have `docker-desktop` running to host kinD kubernetes cluster.
- Provide your S3 bucket names in `eduscan-handler/face_recognition_module.py`.
- Provide your AWS credentials in `eduscan-handler/helper_functions.py`.

## Usage

Follow these steps to run the OpenFaaS function locally:

1. Get kind and kubectl:
   ```
   arkade get kind
   arkade get kubectl
   ```

2. Create kind cluster:
   ```
   kind create cluster --name kind-cluster
   ```

3. Make sure your kubectl context is set to `kind-cluster`.
   ```
   kubectl config use-context kind-kind-cluster
   ```

4. Install OpenFaas with arkade. (Git bash on Windows, Terminal on Linux/MacOS)
   ```
   arkade install openfaas
   ```

5. Make sure you have faas-cli:
   ```
   arkade get faas-cli
   ```

6. Check gateway rollout status and forward the gateway to your machine:
   ```
   kubectl rollout status -n openfaas deploy/gateway
   kubectl port-forward -n openfaas svc/gateway 8080:8080 &
   ```

7. Using basic auth, login to OpenFaas and make note of login credentials to use UI on web browser.
   ```
   PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
   echo -n $PASSWORD | faas-cli login --username admin --password-stdin
   ```
   Make note of the password using: `echo $PASSWORD`

8. **Build and Deploy the Function:**
   Goto `openfaas-setup` folder.
   ```
   faas-cli up -f eduscan-handler.yml
   ```

   This command builds the Docker image and deploys the function to your OpenFaaS cluster.

2. **Access the Function URL:**
   After deploying, OpenFaaS assigns a URL to your function. Retrieve it using:
   ```
   faas-cli describe -f eduscan-handler.yml
   ```
   Look for the "Url" field in the output. The function can be accessed at `http://your-gateway-url:8080/function/eduscan-handler`.

3. **Trigger the Function:**
   - Trigger your function by using `trigger-test.py` script to check if it works. 
   - The script assumes you already have object in pre-configured object `test_0.mp4` in S3 storage.

## Monitoring

1. View logs of OpenFaas function invocations using:
   ```
   faas-cli logs eduscan-handler
   ```

3. **Visualize metrics with Grafana:**
   - Make sure prometheus is installed and running in openfaas namespace.
      ```
      kubectl get pods -n openfaas
      ```

   - Install Grafana in OpenFaas:
      ```
      helm repo add grafana https://grafana.github.io/helm-charts
      helm repo update
      helm install grafana grafana/grafana --namespace=openfaas
      ```

   - Get Grafana login credentials:
      Password: Make note of password
      ```
      kubectl get secret --namespace openfaas grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
      ```
      Login ID: `admin`
   
   - Access Grafana:
      ```
      export POD_NAME=$(kubectl get pods --namespace openfaas -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")

      kubectl --namespace openfaas port-forward $POD_NAME 3000
      ```

      Goto link `http://localhost:3000`. Keep the terminal for port forward open.
   
   - Configure Grafana dashboard for OpenFaas:
      - Add a Data Source.
      - Add prometheus to Data Source. Prometheus url is `http://prometheus.openfaas:9090`. Click "Save & Test".
      - Import OpenFaas dashboard using menu options. "Import via grafana.com" field, enter the OpenFaaS dashboard ID 3434 and click "Load".
      - In the "Options" section, select the Prometheus data source you configured earlier.
      - Click "Import" to import the dashboard.


## Cleanup

To remove the deployed function and associated resources, run:

```bash
faas-cli remove -f eduscan-handler.yml
kind delete cluster --name kind-cluster
```