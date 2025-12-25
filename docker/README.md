# 🐳 Docker Deployment Guide – E-Commerce Data Pipeline

This document explains how to build, run, verify, and manage the E-Commerce Data Pipeline using Docker and Docker Compose.

---

## 1. Prerequisites

Ensure the following are installed on your system:

### Software Requirements
- Docker Engine **v20.10+**
- Docker Compose **v2.0+**
  
#### Verify installation:

```bash
docker --version
docker compose version
```

### System Requirements

Minimum 4 GB RAM

Minimum 5 GB free disk space

**OS:** Windows / Linux / macOS

---
## 2. Project Services Overview

The Docker setup includes the following services:

Service Name	Description
postgres	PostgreSQL database (staging, production, warehouse schemas)
pipeline	Python-based ETL pipeline & orchestrator

***Services communicate using Docker's internal network.***

---

## 3. Quick Start Guide
#### 3.1 Build Docker Images

From the project root:
```
docker compose build
```

#### 3.2 Start Services
```
docker compose up -d
```

This starts:

PostgreSQL database

Pipeline container (waits for DB readiness)

#### 3.3 Verify Running Services
```
docker compose ps
```

***Expected output:***

postgres → healthy

pipeline → running / completed

#### 3.4 Run Pipeline Inside Container

If pipeline does not auto-run:

docker compose exec pipeline python scripts/pipeline_orchestrator.py

#### 3.5 Access PostgreSQL Database
docker compose exec postgres psql -U postgres -d ecommerce_db

To list schemas:
```
\dn
```

#### 3.6 View Logs

Pipeline logs:
```
docker compose logs pipeline
```

Database logs:
```
docker compose logs postgres
```

#### 3.7 Stop Services
```
docker compose down
```

#### 3.8 Cleanup (Volumes & Images)

** This will delete database data.**
```
docker compose down -v
docker system prune -f
```
---
## 4. Configuration Details

**Environment Variables**

Configured via .env file or docker-compose.yml:

DB_HOST=postgres

DB_PORT=5432

DB_NAME=ecommerce_db

DB_USER=postgres

DB_PASSWORD=postgres

**Volume Mounts**
Volume	Purpose
pg_data	Persist PostgreSQL data
./logs	Persist pipeline logs
./data	Persist generated outputs

### Network Configuration

Default Docker bridge network

Services communicate via service names (not IPs)

Resource Limits (Optional)

Can be configured in docker-compose.yml:
```
deploy:
  resources:
    limits:
      memory: 1g
      cpus: "1.0"
```
---
## 5. Health Checks & Dependencies

PostgreSQL includes a healthcheck

Pipeline service uses depends_on with health condition

Pipeline starts only after DB is ready

---

## 6. Troubleshooting

Port Already in Use

***Error:*** bind: address already in use

**Solution:**

Stop local PostgreSQL

Or change port in docker-compose.yml

**Database Not Ready**

**Solution:**
```
docker compose logs postgres
```

Wait until status is healthy.

**Container Fails to Start**
```
docker compose logs pipeline
```

Check:

Missing dependencies

Incorrect environment variables

Volume Permission Issues (Linux)
```
sudo chown -R $USER:$USER data logs
```
Network Connectivity Issues

Ensure pipeline connects using:

```
DB_HOST=postgres
```
(not localhost)

---

## 7. Verification Checklist

✔ docker compose up starts all services
✔ Pipeline waits for DB health check
✔ Data persists after container restart
✔ Logs are accessible
✔ Services communicate via service name

---

## 8. Conclusion

This Docker setup ensures:

Service isolation

Reliable orchestration

Data persistence

Production-ready deployment
