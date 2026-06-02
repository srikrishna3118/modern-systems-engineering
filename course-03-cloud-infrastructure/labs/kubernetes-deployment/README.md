# Lab: Kubernetes Deployment – Infrastructure as Code

## Overview
Containerize and deploy a microservice application to Kubernetes using declarative manifests. Covers Deployments, Services, health probes, and basic inspection/debugging.

## Learning Objectives
- Write Kubernetes manifests (Deployment, Service)
- Use livenessProbe and readinessProbe for health checks
- Scale and update applications declaratively
- Access logs and inspect resources

## Prerequisites
- Docker
- `kubectl`
- Minikube or Kind cluster

## Setup

```bash
cd starter-code
pip install -r requirements.txt
```

## Run

1. Build the image:
	```bash
	docker build -t my-app:1.0 .
	```
2. Complete the TODOs in `k8s/deployment.yaml` and `k8s/service.yaml`.
3. Apply manifests:
	```bash
	kubectl apply -f k8s/
	```

## Validation

```bash
kubectl get pods
kubectl get svc

# Port-forward and hit the service
kubectl port-forward svc/my-app-service 8000:8000
curl -s http://localhost:8000/ | head
```

## Experiment

1. Increase replicas and observe rollout behavior: `kubectl scale deployment/my-app --replicas=5`.
2. Break readinessProbe intentionally and observe traffic drop while pods stay running.

## Solution
See the `solution/` directory for reference manifests.
