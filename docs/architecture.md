
---

```md
# E-Commerce Data Pipeline Architecture

## Overview
This document describes the architecture of the e-commerce data analytics platform.

---

## System Components

### 1. Data Generation Layer
- Generates synthetic data using Python Faker
- Outputs CSV files (customers, products, transactions)

### 2. Data Ingestion Layer
- Loads CSV data into PostgreSQL staging schema
- Technology: Python + SQLAlchemy
- Pattern: Batch ingestion

### 3. Data Storage Layer
- **Staging:** Raw data replica
- **Production:** Cleaned & normalized (3NF)
- **Warehouse:** Star schema for analytics

### 4. Data Processing Layer
- Data quality checks
- Transformations & enrichment
- SCD Type-2 handling
- Aggregation tables for performance

### 5. Data Serving Layer
- Optimized analytical SQL queries
- BI tool connectivity

### 6. Visualization Layer
- Power BI dashboards
- 16+ visuals across 4 pages

### 7. Orchestration Layer
- Pipeline orchestrator
- Scheduled execution
- Monitoring & logging

---

## Data Models

### Staging Model
- Exact CSV replica
- Minimal validation

### Production Model (3NF)
- Eliminates redundancy
- Enforces integrity
- Transactional correctness

### Warehouse Model (Star Schema)
- Fact: fact_sales
- Dimensions: customer, product, date, payment
- Optimized for BI queries

---

## Design Decisions & Rationale

- **PostgreSQL:** Open-source, analytical support, schema isolation
- **Star Schema:** BI-friendly, fast aggregations
- **Layered Schemas:** Auditability, correctness, scalability

---

## Deployment Architecture
- PostgreSQL running in Docker
- Python ETL scripts executed locally or scheduled
