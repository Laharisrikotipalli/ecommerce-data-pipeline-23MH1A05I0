E-Commerce Data Pipeline Project
👤 Student Information

Name: Lahari Sri Kotipalli

Roll Number: 23MH1A05I0

Email: laharisrikotipalli07@gmail.com

Submission Date: 2025-12-25

🔗 GitHub Repository

Repository Name: ecommerce-data-pipeline-23MH1A05I0

Repository URL:

https://github.com/Laharisrikotipalli/ecommerce-data-pipeline-23MH1A05I0


Repository Visibility: Public

Release Tag: v1.0

✅ Project Completion Status (7 Phases)
Phase	Description	Status
Phase 1	Data Generation (CSV creation)	✅ Completed
Phase 2	Data Ingestion (Staging schema)	✅ Completed
Phase 3	Data Transformation (Production schema)	✅ Completed
Phase 4	Data Quality Checks & Reporting	✅ Completed
Phase 5	Warehouse Modeling (Star Schema)	✅ Completed
Phase 6	Orchestration & Scheduling	✅ Completed
Phase 7	BI Dashboard & Analytics	✅ Completed
🧱 Architecture Overview

Schema Design:

staging → raw ingested data

production → cleaned & normalized data

warehouse → star schema (fact & dimensions)

Fact Table: warehouse.fact_sales

Dimensions: dim_customers, dim_products, dim_date, dim_payment_method

Architecture Documentation:

architecture.md

⚙️ Technology Stack

Language: Python 3.9

Database: PostgreSQL 14

Containerization: Docker & Docker Compose

CI/CD: GitHub Actions

Testing: Pytest + pytest-cov

BI Tool: Power BI Desktop / Tableau Public

🐳 Docker Setup

Files Included:

Dockerfile

docker-compose.yml

docker/README.md

Services:

PostgreSQL

Data Pipeline Application

Verification:

Containers start successfully

Database persists using Docker volumes

Pipeline runs end-to-end inside Docker

🔁 CI/CD Pipeline

Workflow File: .github/workflows/ci.yml

Triggers: Push & Pull Request

Pipeline Steps:

Install dependencies

Start PostgreSQL service

Create schemas

Run unit tests

Enforce test coverage

Test Coverage: >80% (PASS)

🧪 Testing Summary

Total Tests: 16

Test Types:

Unit tests

Schema validation tests

Quality checks

Orchestrator tests

Coverage: 81%+

📊 BI Dashboard
Option Used:

✅ Power BI Desktop

Artifacts Provided:

.pbix file

4 dashboard screenshots

Metadata JSON

Dashboards Include:

Executive Overview

Product Performance

Customer Segmentation

Revenue & Trends

Dashboard Guide:

dashboard_guide.md

📁 Data Artifacts Included
Raw Data (CSV)

customers.csv

products.csv

transactions.csv

transaction_items.csv

Pipeline Reports (JSON)

ingestion_summary.json

quality_report.json

transformation_summary.json

pipeline_execution_report.json

monitoring_report.json

Analytical Outputs

10 SQL query result CSV files

▶️ Running Instructions
Local Execution
pip install -r requirements.txt
python scripts/pipeline_orchestrator.py

Docker Execution
docker-compose up --build

Run Tests
pytest tests/ -v

📈 Project Statistics

Total Python Lines of Code: ~XXXX

SQL Scripts: XX

Test Files: XX

Records Processed per Run: ~XXXX

Test Coverage: 81%+

⚠️ Challenges Faced & Solutions
Challenge 1: Database availability in CI

Solution: Used GitHub Actions PostgreSQL service with health checks

Challenge 2: Long-running scheduler in CI

Solution: Disabled scheduler loop during CI runs

Challenge 3: Import path issues

Solution: Proper package structure + PYTHONPATH configuration

Challenge 4: Test coverage enforcement

Solution: Focused coverage on core orchestration logic

🔍 Verification Checklist

 Repository is public

 All required files committed

 .gitignore excludes secrets & logs

 Docker Compose works correctly

 CI pipeline runs successfully

 Tests pass with >80% coverage

 Documentation complete

 Dashboard artifacts included

🏁 Final Notes

This project implements a production-grade data engineering pipeline with:

Clean architecture

Automated testing

Containerized deployment

CI/CD integration

BI-ready warehouse modeling

The solution is fully reproducible, well-documented, and operationally ready.