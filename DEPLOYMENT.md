# Deployment Guide

## Production Deployment

This guide covers deploying the US Visa Prediction Model to production environments.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Kubernetes Deployment](#kubernetes-deployment)
3. [CI/CD Pipeline](#cicd-pipeline)
4. [Monitoring](#monitoring)
5. [Scaling](#scaling)
6. [Rollback Procedures](#rollback-procedures)

## Docker Deployment

### Building the Docker Image

```bash
# Build production image
docker build -t usvisa-app:latest .

# Tag for registry
docker tag usvisa-app:latest your-registry/usvisa-app:v1.0.0

# Push to registry
docker push your-registry/usvisa-app:v1.0.0
```

### Running Docker Container

```bash
# Set environment variables
export MONGODB_URL="mongodb+srv://user:pass@cluster.mongodb.net"
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export ENVIRONMENT="production"

# Run container
docker run -d \
  -p 8080:8080 \
  -e MONGODB_URL=$MONGODB_URL \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e ENVIRONMENT=production \
  --name usvisa-app \
  your-registry/usvisa-app:v1.0.0
```

### Docker Compose for Production

```bash
# Create production .env file
cp .env.example .env.prod
# Edit .env.prod with production values

# Deploy services
docker-compose -f docker-compose.yml up -d
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Docker registry access
- Helm (optional, but recommended)

### Step 1: Create Namespace and Secrets

```bash
# Create namespace
kubectl create namespace usvisa-app

# Create secrets from .env
kubectl create secret generic usvisa-secrets \
  --from-literal=MONGODB_URL='mongodb+srv://...' \
  --from-literal=AWS_ACCESS_KEY_ID='...' \
  --from-literal=AWS_SECRET_ACCESS_KEY='...' \
  --from-literal=SECRET_KEY='...' \
  -n usvisa-app
```

### Step 2: Deploy Application

```bash
# Update image in deployment.yaml
# Edit k8s/deployment.yaml and change:
# image: your-registry/usvisa-app:v1.0.0

# Apply deployment
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n usvisa-app
kubectl get svc -n usvisa-app
```

### Step 3: Configure Ingress

```bash
# Update hostname in k8s/ingress.yaml
# host: your-domain.com

# Apply ingress
kubectl apply -f k8s/ingress.yaml

# Check ingress status
kubectl get ingress -n usvisa-app
```

### Step 4: Setup Certificate (Let's Encrypt)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Step 5: Verify Deployment

```bash
# Check pod status
kubectl get pods -n usvisa-app -w

# View logs
kubectl logs -n usvisa-app -l app=usvisa-app --tail=100 -f

# Check service endpoints
kubectl get endpoints -n usvisa-app usvisa-app

# Test health check
kubectl port-forward -n usvisa-app svc/usvisa-app 8080:80
curl http://localhost:8080/health
```

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes GitHub Actions workflows in `.github/workflows/aws.yaml`:

1. **Continuous Integration**
   - Run tests
   - Build Docker image
   - Push to ECR

2. **Continuous Deployment**
   - Deploy to EC2 or ECS
   - Update running containers
   - Health checks

### Setting up Secrets in GitHub

1. Go to Settings → Secrets and variables → Actions
2. Add required secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION`
   - `ECR_REPO`
   - `MONGODB_URL`

## Monitoring

### Prometheus Metrics

Metrics available at `http://localhost:8080/metrics`:

```
# Prediction metrics
visa_predictions_total{prediction_result="Visa-approved"} 150
visa_prediction_latency_seconds{} 0.245

# Training metrics
model_training_total{status="success"} 5

# System metrics
active_requests 3
```

### Grafana Dashboards

1. Access Grafana: http://localhost:3000
2. Add Prometheus data source
3. Import dashboard: `k8s/grafana-dashboard.json`

### Health Checks

```bash
# API health
curl http://localhost:8080/health

# Database health
curl http://localhost:8080/api/status
```

### Logging

Structured logs available in:
- Console output
- `logs/*.log` (plain text)
- `logs/*.json` (structured JSON)

## Scaling

### Horizontal Scaling with Kubernetes

```bash
# Manual scaling
kubectl scale deployment usvisa-app --replicas=5 -n usvisa-app

# Auto-scaling (configured in deployment)
kubectl get hpa -n usvisa-app
```

### Load Balancing

The ingress controller handles load balancing automatically.

Verify with:
```bash
kubectl get ingress -n usvisa-app -o wide
```

## Rollback Procedures

### Kubernetes Rollback

```bash
# View rollout history
kubectl rollout history deployment/usvisa-app -n usvisa-app

# Rollback to previous version
kubectl rollout undo deployment/usvisa-app -n usvisa-app

# Rollback to specific revision
kubectl rollout undo deployment/usvisa-app --to-revision=2 -n usvisa-app

# Check rollout status
kubectl rollout status deployment/usvisa-app -n usvisa-app
```

### Docker Container Rollback

```bash
# Stop current container
docker stop usvisa-app

# Start previous version
docker run -d \
  --name usvisa-app \
  your-registry/usvisa-app:v1.0.0
```

## Performance Optimization

### Resource Limits

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Auto-scaling Configuration

```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      averageUtilization: 70
```

## Security Best Practices

1. **Secret Management**
   - Use Kubernetes secrets
   - Rotate credentials regularly
   - Never commit secrets

2. **Network Policies**
   - Restrict pod-to-pod communication
   - Use NetworkPolicy resources
   - Implement RBAC

3. **Image Security**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Don't run as root

4. **SSL/TLS**
   - Use cert-manager
   - Let's Encrypt certificates
   - Enable HTTPS only

## Troubleshooting

### Deployment Issues

```bash
# Check events
kubectl describe deployment usvisa-app -n usvisa-app

# Check pod status
kubectl describe pod <pod-name> -n usvisa-app

# View logs
kubectl logs <pod-name> -n usvisa-app
```

### Performance Issues

```bash
# Check resource usage
kubectl top pods -n usvisa-app
kubectl top nodes

# Check metrics
kubectl get hpa -n usvisa-app
```

### Connectivity Issues

```bash
# Test DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup usvisa-app

# Test connectivity
kubectl exec -it <pod-name> -n usvisa-app -- curl http://localhost:8080/health
```

## Backup and Recovery

### Database Backup

```bash
# Backup MongoDB
mongodump --uri="mongodb+srv://..." --out=/backup

# Restore MongoDB
mongorestore --uri="mongodb+srv://..." /backup
```

### Configuration Backup

```bash
# Backup Kubernetes resources
kubectl get all -n usvisa-app -o yaml > backup.yaml

# Restore from backup
kubectl apply -f backup.yaml
```

---

For more information, see [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md)
