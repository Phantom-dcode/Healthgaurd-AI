# 🚀 HealthGuard AI - Production Deployment Guide

## Prerequisites
- Docker & Docker Compose installed
- AWS Account (optional, for cloud deployment)
- PostgreSQL 15+ (or use managed RDS)
- Node.js 18+ & Python 3.11+
- Git

---

## 📋 Deployment Checklist

### Phase 1: Local Testing (Before Deployment)
- [ ] Clone repository: `git clone https://github.com/Phantom-dcode/Healthgaurd-AI.git`
- [ ] Copy `.env.example` to `.env` in backend folder
- [ ] Generate secure SECRET_KEY: `openssl rand -hex 32`
- [ ] Update DATABASE_URL with your credentials
- [ ] Run locally: `docker-compose up --build`
- [ ] Test API at `http://localhost:8000/docs`
- [ ] Test Frontend at `http://localhost:5173`

### Phase 2: Production Environment Setup

#### 2.1 AWS Setup (ECS + RDS + S3)

**Create RDS PostgreSQL Database:**
```bash
# AWS Console → RDS → Create Database
# Engine: PostgreSQL 15
# Multi-AZ: Yes (for production)
# Storage: 100 GB (gp3)
# Backup retention: 30 days
# Enable encryption at rest
```

**Create S3 Bucket for Reports:**
```bash
# AWS Console → S3 → Create Bucket
# Name: healthguard-reports-prod
# Region: us-east-1
# Block public access: Yes
# Versioning: Enabled
# Server-side encryption: AES-256
```

**Create IAM User for Application:**
```bash
# AWS Console → IAM → Users → Create User
# Policy: Custom policy with S3 and CloudWatch permissions
```

#### 2.2 Environment Variables (Production)

**Backend .env (DO NOT COMMIT):**
```env
# Application
APP_NAME="HealthGuard AI"
APP_VERSION="1.0.0"
DEBUG=False
ENVIRONMENT=production

# Database (RDS)
DATABASE_URL=postgresql://admin:STRONG_PASSWORD@healthguard-prod.xxxxx.us-east-1.rds.amazonaws.com:5432/healthguard_prod

# Security
SECRET_KEY=your-generated-32-char-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS - Update with your domain
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# AWS
AWS_ACCESS_KEY_ID=your-iam-access-key
AWS_SECRET_ACCESS_KEY=your-iam-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=healthguard-reports-prod

# Logging
LOG_LEVEL=INFO
```

**Frontend .env (Production):**
```env
VITE_API_URL=https://api.yourdomain.com/api/v1
```

### Phase 3: Docker Build & Push to Registry

#### 3.1 Build Docker Images

```bash
# Build Backend
cd backend
docker build -t healthguard-backend:1.0.0 -f Dockerfile.prod .
docker tag healthguard-backend:1.0.0 YOUR_DOCKER_REGISTRY/healthguard-backend:latest

# Build Frontend
cd ../frontend
docker build -f Dockerfile.prod -t healthguard-frontend:1.0.0 .
docker tag healthguard-frontend:1.0.0 YOUR_DOCKER_REGISTRY/healthguard-frontend:latest
```

#### 3.2 Push to Docker Registry (AWS ECR)

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Push Backend
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthguard-backend:latest

# Push Frontend
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthguard-frontend:latest
```

### Phase 4: Deploy to AWS ECS

#### 4.1 Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name healthguard-prod --region us-east-1
```

#### 4.2 Create Task Definitions

**Backend Task Definition (healthguard-backend-task.json):**
```json
{
  "family": "healthguard-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthguard-backend:latest",
      "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"},
        {"name": "AWS_REGION", "value": "us-east-1"}
      ],
      "secrets": [
        {"name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:healthguard/SECRET_KEY"},
        {"name": "DATABASE_URL", "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:healthguard/DATABASE_URL"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/healthguard-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 4.3 Create ECS Service

```bash
aws ecs create-service \
  --cluster healthguard-prod \
  --service-name healthguard-backend-service \
  --task-definition healthguard-backend \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx,subnet-yyyyy],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:ACCOUNT:targetgroup/healthguard/xxxxx,containerName=backend,containerPort=8000
```

### Phase 5: Setup Application Load Balancer (ALB)

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name healthguard-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --scheme internet-facing \
  --type application

# Create Target Groups
aws elbv2 create-target-group \
  --name healthguard-backend-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx

aws elbv2 create-target-group \
  --name healthguard-frontend-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-xxxxx

# Create Listeners
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:.../targetgroup/healthguard-backend-tg/...
```

### Phase 6: Setup CloudFront CDN

```bash
# Create CloudFront Distribution
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

### Phase 7: Domain & SSL Certificate

1. **Register Domain** (Route 53 or external provider)
2. **Create SSL Certificate** (AWS Certificate Manager)
3. **Add DNS Records** in Route 53:
   ```
   api.yourdomain.com → ALB DNS
   www.yourdomain.com → CloudFront Distribution
   yourdomain.com → CloudFront Distribution
   ```

### Phase 8: Monitoring & Auto-Scaling

#### 8.1 CloudWatch Monitoring

```bash
# Create CloudWatch Alarms
aws cloudwatch put-metric-alarm \
  --alarm-name healthguard-high-cpu \
  --alarm-description "Alert when CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

#### 8.2 Auto-Scaling Policy

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/healthguard-prod/healthguard-backend-service \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --policy-name healthguard-scale-policy \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/healthguard-prod/healthguard-backend-service \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

### Phase 9: Database Migration

```bash
# SSH into backend container
docker exec healthguard-backend bash

# Run migrations
alembic upgrade head

# Seed initial data (if needed)
python -m app.scripts.seed_db
```

### Phase 10: Backup & Disaster Recovery

```bash
# Enable RDS Automated Backups (30 days retention)
aws rds modify-db-instance \
  --db-instance-identifier healthguard-prod \
  --backup-retention-period 30 \
  --apply-immediately

# Create Read Replica for disaster recovery
aws rds create-db-instance-read-replica \
  --db-instance-identifier healthguard-prod-replica \
  --source-db-instance-identifier healthguard-prod \
  --db-instance-class db.t3.micro
```

---

## ✅ Post-Deployment Verification

```bash
# 1. Check API Health
curl https://api.yourdomain.com/api/v1/health

# 2. Test Authentication
curl -X POST https://api.yourdomain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@healthguard.ai","password":"Admin@123"}'

# 3. Monitor Logs
aws logs tail /ecs/healthguard-backend --follow

# 4. Check ECS Service Status
aws ecs describe-services \
  --cluster healthguard-prod \
  --services healthguard-backend-service

# 5. Test Frontend at https://yourdomain.com
```

---

## 🔧 Troubleshooting

### Backend Service Won't Start
```bash
# Check logs
aws logs tail /ecs/healthguard-backend --follow

# Verify environment variables
aws ecs describe-task-definition --task-definition healthguard-backend:latest

# Test database connection
python -c "import psycopg2; psycopg2.connect(DATABASE_URL)"
```

### Database Connection Issues
```bash
# Check RDS security group
aws ec2 describe-security-groups --group-ids sg-xxxxx

# Ensure ECS security group can reach RDS
# Add ingress rule: Port 5432, Source: ECS security group
```

### Frontend Not Loading
```bash
# Check CloudFront distribution status
aws cloudfront get-distribution --id XXXXX

# Invalidate cache
aws cloudfront create-invalidation --distribution-id XXXXX --paths "/*"
```

---

## 📈 Performance Optimization

- **Enable Redis Cache** for sessions and API responses
- **Enable CDN Caching** for static assets (1 year)
- **Database Indexing** on frequently queried columns
- **Connection Pooling** (PgBouncer)
- **API Rate Limiting** (prevent abuse)
- **Compression** (gzip for responses)

---

## 🔐 Security Checklist

- [ ] All secrets in AWS Secrets Manager (not in code)
- [ ] SSL/TLS enabled on all endpoints
- [ ] CORS properly configured
- [ ] WAF rules enabled on ALB
- [ ] Regular security patches applied
- [ ] Database encrypted at rest & in transit
- [ ] VPC properly configured (private subnets for DB)
- [ ] MFA enabled on AWS console
- [ ] CloudTrail logging enabled
- [ ] Regular backups tested

---

## 📞 Support & Monitoring

- **Uptime Monitoring**: StatusPage.io or UptimeRobot
- **Error Tracking**: Sentry.io integration
- **Logs**: CloudWatch with custom dashboards
- **Alerts**: SNS notifications for critical errors
- **Performance**: DataDog or New Relic APM

---

**Deployment Status**: Ready for Production ✅
