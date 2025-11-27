# 🐳 Docker Deployment Guide

Complete guide for deploying the Sentiment Chatbot using Docker on various cloud platforms.

---

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [AWS Deployment](#aws-deployment)
- [Google Cloud Platform](#google-cloud-platform)
- [Azure Deployment](#azure-deployment)
- [DigitalOcean](#digitalocean)
- [Docker Hub](#docker-hub)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 10GB disk space

### Local Deployment

1. **Clone Repository**
   ```bash
   git clone <your-repo-url>
   cd sentiment-chatbot
   ```

2. **Create Environment File**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Build and Run**
   ```bash
   docker-compose up -d
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000

5. **View Logs**
   ```bash
   docker-compose logs -f
   ```

6. **Stop Services**
   ```bash
   docker-compose down
   ```

---

## 💻 Local Development

### Build Individual Services

**Backend Only:**
```bash
cd backend
docker build -t sentiment-chatbot-backend .
docker run -p 5000:5000 --env-file ../.env sentiment-chatbot-backend
```

**Frontend Only:**
```bash
cd frontend
docker build -t sentiment-chatbot-frontend .
docker run -p 3000:80 sentiment-chatbot-frontend
```

### Development with Hot Reload

For development, use volume mounts:

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    environment:
      - FLASK_ENV=development
    command: python app.py
    
  frontend:
    build: ./frontend
    volumes:
      - ./frontend/src:/app/src
    command: npm run dev
```

Run with:
```bash
docker-compose -f docker-compose.dev.yml up
```

---

## ☁️ AWS Deployment

### Option 1: AWS ECS (Elastic Container Service)

#### Step 1: Push Images to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create repositories
aws ecr create-repository --repository-name sentiment-chatbot-backend
aws ecr create-repository --repository-name sentiment-chatbot-frontend

# Build and tag images
docker build -t sentiment-chatbot-backend ./backend
docker tag sentiment-chatbot-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiment-chatbot-backend:latest

docker build -t sentiment-chatbot-frontend ./frontend
docker tag sentiment-chatbot-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiment-chatbot-frontend:latest

# Push images
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiment-chatbot-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiment-chatbot-frontend:latest
```

#### Step 2: Create ECS Task Definition

Create `task-definition.json`:

```json
{
  "family": "sentiment-chatbot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiment-chatbot-backend:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "GROQ_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:groq-api-key"
        },
        {
          "name": "GMAIL_TOKEN",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:gmail-token"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/sentiment-chatbot",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "backend"
        }
      }
    },
    {
      "name": "frontend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/sentiment-chatbot-frontend:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/sentiment-chatbot",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "frontend"
        }
      }
    }
  ]
}
```

#### Step 3: Deploy to ECS

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create ECS cluster
aws ecs create-cluster --cluster-name sentiment-chatbot-cluster

# Create service
aws ecs create-service \
  --cluster sentiment-chatbot-cluster \
  --service-name sentiment-chatbot-service \
  --task-definition sentiment-chatbot \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Option 2: AWS EC2 with Docker

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <your-repo-url>
cd sentiment-chatbot

# Create .env file
nano .env
# Add your environment variables

# Deploy
docker-compose up -d

# Setup auto-restart on reboot
sudo systemctl enable docker
```

### Option 3: AWS App Runner

```bash
# Create apprunner.yaml
cat > apprunner.yaml << EOF
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  command: gunicorn --bind 0.0.0.0:8080 app:app
  network:
    port: 8080
EOF

# Deploy using AWS Console or CLI
aws apprunner create-service \
  --service-name sentiment-chatbot \
  --source-configuration file://apprunner-config.json
```

---

## 🌐 Google Cloud Platform (GCP)

### Option 1: Cloud Run

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push backend
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sentiment-chatbot-backend

# Deploy backend
gcloud run deploy sentiment-chatbot-backend \
  --image gcr.io/YOUR_PROJECT_ID/sentiment-chatbot-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=$GROQ_API_KEY,GMAIL_TOKEN=$GMAIL_TOKEN

# Build and push frontend
cd ../frontend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sentiment-chatbot-frontend

# Deploy frontend
gcloud run deploy sentiment-chatbot-frontend \
  --image gcr.io/YOUR_PROJECT_ID/sentiment-chatbot-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 2: GKE (Google Kubernetes Engine)

```bash
# Create cluster
gcloud container clusters create sentiment-chatbot-cluster \
  --num-nodes=2 \
  --machine-type=e2-medium \
  --region=us-central1

# Get credentials
gcloud container clusters get-credentials sentiment-chatbot-cluster --region=us-central1

# Create Kubernetes deployment
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Expose service
kubectl expose deployment sentiment-chatbot --type=LoadBalancer --port=80
```

---

## 🔷 Azure Deployment

### Option 1: Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name sentiment-chatbot-rg --location eastus

# Create container registry
az acr create --resource-group sentiment-chatbot-rg \
  --name sentimentchatbotacr --sku Basic

# Login to ACR
az acr login --name sentimentchatbotacr

# Build and push images
docker build -t sentimentchatbotacr.azurecr.io/backend:latest ./backend
docker push sentimentchatbotacr.azurecr.io/backend:latest

docker build -t sentimentchatbotacr.azurecr.io/frontend:latest ./frontend
docker push sentimentchatbotacr.azurecr.io/frontend:latest

# Deploy container group
az container create \
  --resource-group sentiment-chatbot-rg \
  --name sentiment-chatbot \
  --image sentimentchatbotacr.azurecr.io/backend:latest \
  --dns-name-label sentiment-chatbot \
  --ports 5000 \
  --environment-variables GROQ_API_KEY=$GROQ_API_KEY
```

### Option 2: Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name sentiment-chatbot-plan \
  --resource-group sentiment-chatbot-rg \
  --is-linux \
  --sku B1

# Create web app
az webapp create \
  --resource-group sentiment-chatbot-rg \
  --plan sentiment-chatbot-plan \
  --name sentiment-chatbot-app \
  --deployment-container-image-name sentimentchatbotacr.azurecr.io/backend:latest

# Configure environment variables
az webapp config appsettings set \
  --resource-group sentiment-chatbot-rg \
  --name sentiment-chatbot-app \
  --settings GROQ_API_KEY=$GROQ_API_KEY
```

---

## 🌊 DigitalOcean

### Option 1: App Platform

```bash
# Install doctl
# https://docs.digitalocean.com/reference/doctl/how-to/install/

# Login
doctl auth init

# Create app spec
cat > .do/app.yaml << EOF
name: sentiment-chatbot
services:
- name: backend
  github:
    repo: your-username/sentiment-chatbot
    branch: main
    deploy_on_push: true
  dockerfile_path: backend/Dockerfile
  http_port: 5000
  instance_count: 1
  instance_size_slug: basic-xxs
  env:
  - key: GROQ_API_KEY
    value: \${GROQ_API_KEY}
    type: SECRET
  - key: GMAIL_TOKEN
    value: \${GMAIL_TOKEN}
    type: SECRET

- name: frontend
  github:
    repo: your-username/sentiment-chatbot
    branch: main
  dockerfile_path: frontend/Dockerfile
  http_port: 80
  instance_count: 1
  instance_size_slug: basic-xxs
EOF

# Deploy
doctl apps create --spec .do/app.yaml
```

### Option 2: Droplet with Docker

```bash
# Create droplet
doctl compute droplet create sentiment-chatbot \
  --image docker-20-04 \
  --size s-1vcpu-1gb \
  --region nyc1

# SSH into droplet
doctl compute ssh sentiment-chatbot

# Clone and deploy
git clone <your-repo-url>
cd sentiment-chatbot
docker-compose up -d
```

---

## 🐋 Docker Hub

### Push Images to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag images
docker tag sentiment-chatbot-backend:latest yourusername/sentiment-chatbot-backend:latest
docker tag sentiment-chatbot-frontend:latest yourusername/sentiment-chatbot-frontend:latest

# Push images
docker push yourusername/sentiment-chatbot-backend:latest
docker push yourusername/sentiment-chatbot-frontend:latest

# Update docker-compose.yml to use Docker Hub images
# image: yourusername/sentiment-chatbot-backend:latest
```

### Pull and Run from Docker Hub

```bash
# On any machine with Docker
docker pull yourusername/sentiment-chatbot-backend:latest
docker pull yourusername/sentiment-chatbot-frontend:latest

docker-compose up -d
```

---

## 🔧 Environment Variables

Create `.env` file in project root:

```env
# Required
GROQ_API_KEY=gsk_your_groq_api_key
GMAIL_TOKEN={"token":"ya29...","refresh_token":"1//..."}
EMAIL_SENDER=your-email@gmail.com
JWT_SECRET=your-super-secret-key

# Optional
FLASK_ENV=production
DATABASE_PATH=/app/data/chatbot.db
FRONTEND_URL=https://your-domain.com
```

---

## 🔍 Monitoring & Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats sentiment-chatbot-backend
```

### Health Checks

```bash
# Backend health
curl http://localhost:5000/api/health

# Frontend health
curl http://localhost:3000/health
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Inspect container
docker inspect sentiment-chatbot-backend

# Check if port is in use
netstat -tulpn | grep 5000
```

### Database Issues

```bash
# Access container
docker exec -it sentiment-chatbot-backend bash

# Check database
ls -la /app/data/
sqlite3 /app/data/chatbot.db ".tables"
```

### Network Issues

```bash
# Check networks
docker network ls

# Inspect network
docker network inspect sentiment-chatbot_chatbot-network

# Test connectivity
docker exec sentiment-chatbot-frontend ping backend
```

### Rebuild Containers

```bash
# Rebuild without cache
docker-compose build --no-cache

# Recreate containers
docker-compose up -d --force-recreate
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi sentiment-chatbot-backend sentiment-chatbot-frontend

# Clean system
docker system prune -a
```

---

## 📊 Performance Optimization

### Production Settings

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        max_attempts: 3
    
  frontend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### Enable Caching

Add to nginx.conf:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
```

---

## 🔒 Security Best Practices

1. **Use Secrets Management**
   - AWS Secrets Manager
   - Azure Key Vault
   - GCP Secret Manager

2. **Non-Root User**
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

3. **Scan Images**
   ```bash
   docker scan sentiment-chatbot-backend
   ```

4. **Update Base Images**
   ```bash
   docker pull python:3.11-slim
   docker pull node:18-alpine
   docker pull nginx:alpine
   ```

---

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale backend to 3 instances
docker-compose up -d --scale backend=3

# With load balancer
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Load Balancer Configuration

```yaml
# docker-compose.scale.yml
services:
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

---

## 💰 Cost Estimation

### AWS ECS Fargate
- **0.5 vCPU, 1GB RAM**: ~$15/month
- **Data transfer**: ~$5/month
- **Total**: ~$20/month

### Google Cloud Run
- **Pay per request**: ~$10-20/month (moderate traffic)
- **Always-on**: ~$25/month

### DigitalOcean App Platform
- **Basic tier**: $5/month per service
- **Total**: $10/month (2 services)

### Self-hosted VPS
- **DigitalOcean Droplet**: $6/month (1GB RAM)
- **AWS EC2 t3.micro**: ~$8/month
- **Azure B1S**: ~$8/month

---

## ✅ Deployment Checklist

- [ ] Docker and Docker Compose installed
- [ ] Environment variables configured
- [ ] Images built successfully
- [ ] Containers running without errors
- [ ] Health checks passing
- [ ] Database persisting data
- [ ] Frontend accessible
- [ ] Backend API responding
- [ ] CORS configured correctly
- [ ] SSL/TLS certificate installed (production)
- [ ] Monitoring and logging setup
- [ ] Backup strategy in place

---

**Ready to deploy! 🚀**

Choose your preferred platform and follow the guide above.
