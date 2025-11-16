# Flask Kubernetes CI/CD Pipeline

A complete end-to-end CI/CD pipeline implementation for a Flask application using GitHub Actions, Jenkins, Docker, and Kubernetes. This project demonstrates automated testing, building, and deployment to a Kubernetes cluster with features like rolling updates, scaling, and load balancing.

## Project Description

This project implements a production-ready CI/CD pipeline for a simple Flask "Hello, World!" application. The pipeline includes:

- **Continuous Integration (CI)**: Automated testing and building using GitHub Actions
- **Continuous Delivery (CD)**: Automated deployment to Kubernetes using Jenkins
- **Containerization**: Multi-stage Docker builds for optimized images
- **Orchestration**: Kubernetes deployment with advanced features like rolling updates, scaling, and load balancing

## Kubernetes Features Used

### 1. Rolling Updates

The deployment uses a `RollingUpdate` strategy with:

- **maxSurge: 1**: Allows one additional pod to be created during updates
- **maxUnavailable: 1**: Ensures at least one pod remains available during updates

This ensures zero-downtime deployments where new versions are gradually rolled out while maintaining service availability.

### 2. Scaling

- **Multiple Replicas**: The deployment is configured with 3 replicas by default
- **Horizontal Scaling**: Pods can be scaled up or down using `kubectl scale` command
- **Resource Management**: CPU and memory limits/requests ensure efficient resource utilization

### 3. Load Balancing

- **NodePort Service**: Exposes the application on a static port (30080) on each node
- **Service Discovery**: Kubernetes automatically distributes traffic across all healthy pods
- **Health Probes**: Liveness and readiness probes ensure only healthy pods receive traffic

### 4. Resource Management

- **Resource Requests**: Minimum resources guaranteed (128Mi memory, 100m CPU)
- **Resource Limits**: Maximum resources allowed (256Mi memory, 200m CPU)
- **Health Checks**: Liveness and readiness probes monitor pod health

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.11+**
- **Docker Desktop** (for local development)
- **Minikube** (for local Kubernetes cluster)
- **kubectl** (Kubernetes command-line tool)
- **Jenkins** (for CI/CD pipeline)
- **Git** (for version control)

## Building and Running Locally Using Docker

### Step 1: Clone the Repository

```bash
git clone https://github.com/haiderniaz/flask-k8s-ci-cd-assignment.git
cd flask-k8s-ci-cd-assignment
```

### Step 2: Build the Docker Image

```bash
docker build -t flask-app:latest .
```

This command:

- Uses the multi-stage Dockerfile to create an optimized image
- Installs dependencies in the builder stage
- Copies only necessary files to the final runtime image
- Results in a smaller, more secure production image

### Step 3: Run the Container

```bash
docker run -d -p 8080:8080 --name flask-app flask-app:latest
```

### Step 4: Test the Application

```bash
curl http://localhost:8080
```

You should see: `Hello, World!`

### Step 5: Stop and Remove the Container

```bash
docker stop flask-app
docker rm flask-app
```

## Deploying to Kubernetes Using Jenkins Pipeline

### Prerequisites for Jenkins Deployment

1. **Minikube must be running**:

   ```bash
   minikube start
   minikube status
   ```

2. **kubectl must be configured**:

   ```bash
   kubectl get nodes
   ```

3. **Docker must be accessible** to Jenkins

### Step 1: Configure Jenkins Job

1. Open Jenkins dashboard
2. Create a new **Pipeline** job named `flask-k8s-deployment`
3. In the job configuration:
   - **Pipeline Definition**: Select "Pipeline script from SCM"
   - **SCM**: Select "Git"
   - **Repository URL**: `https://github.com/haiderniaz/flask-k8s-ci-cd-assignment.git`
   - **Branches to build**: `*/main`
   - **Script Path**: `Jenkinsfile`
4. Save the configuration

### Step 2: Configure Jenkins Environment

Ensure Jenkins has access to Docker and kubectl:

1. Go to **Manage Jenkins** → **Configure System**
2. Under **Global properties**, check **Environment variables**
3. Add:
   - **Name**: `PATH`
   - **Value**: `/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH`

### Step 3: Trigger the Pipeline

**Manual Trigger**

1. Go to the Jenkins job page
2. Click **Build Now**

### Step 4: Monitor the Pipeline

The Jenkins pipeline executes three stages:

1. **Build Docker Image**: Builds the Docker image from the Dockerfile
2. **Deploy to Kubernetes**: Applies Kubernetes manifests using `kubectl apply`
3. **Verify Deployment**: Checks rollout status, pods, and services

View the console output to see real-time progress.

### Step 5: Verify Deployment

After successful pipeline execution:

```bash
# Check pods
kubectl get pods -l app=flask-app

# Check services
kubectl get services -l app=flask-app

# Check deployment status
kubectl get deployments flask-app

# Get service URL
minikube service flask-app-service --url
```

### Step 6: Access the Application

```bash
# Get the NodePort URL
minikube service flask-app-service --url

# Or access directly via NodePort
curl http://$(minikube ip):30080
```

## Automated Rollouts, Scaling, and Load Balancing

### Automated Rollouts

The deployment uses a **RollingUpdate** strategy that automatically:

1. **Gradually replaces old pods** with new ones during updates
2. **Maintains service availability** by ensuring at least one pod is always available
3. **Rolls back automatically** if new pods fail health checks
4. **Tracks rollout history** for easy rollback if needed

**Example Rollout:**

```bash
# Trigger a rollout (e.g., after updating the image)
kubectl set image deployment/flask-app flask-app=flask-app:v2

# Monitor rollout status
kubectl rollout status deployment/flask-app

# View rollout history
kubectl rollout history deployment/flask-app

# Rollback if needed
kubectl rollout undo deployment/flask-app
```

### Scaling

Kubernetes allows dynamic scaling of the application:

```bash
# Scale up to 5 replicas
kubectl scale deployment flask-app --replicas=5

# Scale down to 2 replicas
kubectl scale deployment flask-app --replicas=2

# Auto-scaling (requires metrics server)
kubectl autoscale deployment flask-app --min=2 --max=10 --cpu-percent=80
```

**Benefits:**

- **Horizontal Scaling**: Add more pods to handle increased load
- **Resource Efficiency**: Scale down during low traffic periods
- **High Availability**: Multiple replicas ensure service continuity

### Load Balancing

The **NodePort Service** automatically:

1. **Distributes traffic** across all healthy pods using round-robin
2. **Health checks** ensure traffic only goes to ready pods
3. **Service discovery** allows pods to find each other by service name
4. **External access** via NodePort (30080) on any cluster node

**How it works:**

- Kubernetes Service acts as a load balancer
- Traffic to the service is automatically distributed to backend pods
- If a pod becomes unhealthy, it's removed from the load balancer pool
- New pods are automatically added when they become ready

**Testing Load Balancing:**

```bash
# Access the service multiple times to see different pods handling requests
for i in {1..10}; do
  curl http://$(minikube ip):30080
  echo ""
done
```

## Project Structure

```
flask-k8s-ci-cd-assignment/
├── app.py                      # Flask application
├── utils.py                    # Utility functions
├── test_utils.py               # Unit tests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage Docker build
├── Jenkinsfile                 # Jenkins pipeline definition
├── README.md                   # This file
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI workflow
└── kubernetes/
    ├── deployment.yaml         # Kubernetes deployment manifest
    └── service.yaml        # Kubernetes service manifest
```

## CI/CD Pipeline Flow

1. **Developer pushes code** to feature branch
2. **GitHub Actions** triggers automatically:
   - Runs flake8 linting (max line length: 90)
   - Runs pytest unit tests
   - Builds Docker image
3. **Pull Request** created to develop/main
4. **After merge to main**, Jenkins pipeline triggers:
   - Builds Docker image
   - Deploys to Kubernetes
   - Verifies deployment status
5. **Application** is live and accessible via NodePort

## Testing

### Run Unit Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run linting
flake8 --max-line-length=90 app.py utils.py test_utils.py
```

### Test Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f kubernetes/

# Check deployment
kubectl get all -l app=flask-app

# Test the service
curl http://$(minikube ip):30080
```

## Troubleshooting

### Jenkins can't find Docker

- Ensure Docker Desktop is running
- Add Docker path to Jenkins environment variables
- Check Jenkins has permission to access Docker socket

### kubectl commands fail in Jenkins

- Verify minikube is running: `minikube status`
- Check kubectl is in PATH: `which kubectl`
- Ensure Jenkins user has access to kubectl config

### Pods not starting

```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

### Service not accessible

```bash
# Check service
kubectl get svc flask-app-service

# Check endpoints
kubectl get endpoints flask-app-service

# Verify pods are ready
kubectl get pods -l app=flask-app
```

## Contributing

1. Create a feature branch from `develop`
2. Make your changes
3. Ensure tests pass
4. Create a pull request to `develop`
5. After review, merge to `develop`
6. Merge `develop` to `main` for deployment

## License

This project is part of a Cloud MLOps course assignment.

## Authors

- Developer: Abdullah Mazhar
- Admin: Haider Naiz
