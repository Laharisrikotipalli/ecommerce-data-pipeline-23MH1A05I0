E-COMMERCE DATA ANALYTICS PIPELINE

PROJECT OVERVIEW
This project implements an end-to-end E-Commerce Data Analytics Pipeline that generates synthetic data, ingests it into PostgreSQL, processes it across staging, production, and warehouse layers, and visualizes insights using Power BI.

The pipeline follows modern data engineering best practices including:
- Data Generation
- Data Ingestion
- Staging, Production, and Warehouse Schemas
- Orchestration and Monitoring
- Automated Testing
- Docker Containerization
- BI Visualization using Power BI

--------------------------------------------------

ARCHITECTURE OVERVIEW
The pipeline follows a three-layer architecture:
- Staging Layer
- Production Layer
- Warehouse Layer

The warehouse is modeled using a star schema with fact and dimension tables to support analytical queries and BI dashboards.

--------------------------------------------------

PROJECT STRUCTURE

ecommerce-data-pipeline/
├── config/
│   └── config.yaml
├── dashboards/
│   ├── powerbi/
│   │   └── ecommerce_analytics.pbix
│   └── screenshots/
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── transactions.csv
│   │   └── transaction_items.csv
│   ├── staging/
│   └── processed/
│       ├── analytics/
│       ├── pipeline_execution_report.json
│       ├── transformation_summary.json
│       └── quality_reports/
├── scripts/
│   ├── data_generation/
│   │   └── generate_data.py
│   ├── ingestion/
│   │   └── ingest_to_staging.py
│   ├── transformation/
│   │   └── staging_to_production.py
│   ├── quality_checks/
│   │   └── validate_data.py
│   ├── monitoring/
│   │   └── pipeline_monitor.py
│   └── orchestration/
│       └── run_pipeline.py
├── sql/
│   ├── ddl/
│   ├── dml/
│   └── queries/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
├── README.md
└── SUBMISSION.md

--------------------------------------------------

CODE ORGANIZATION
Each folder has a single responsibility:
- data_generation: creates synthetic datasets
- ingestion: loads raw data into staging tables
- transformation: moves data to production and warehouse layers
- quality_checks: validates data quality and integrity
- orchestration: runs the entire pipeline end-to-end
- monitoring: tracks execution and health
- sql: contains DDL, DML, and analytical queries
- tests: unit and integration tests

--------------------------------------------------

CONFIGURATION
- Database credentials are managed using environment variables
- Configuration values are centralized in config/config.yaml
- Docker provides a consistent execution environment

--------------------------------------------------

PREREQUISITES
- Python 3.9 or higher
- Docker and Docker Compose
- Power BI Desktop

--------------------------------------------------

INSTALLATION AND SETUP

Clone the repository:
git clone https://github.com/Laharisrikotipalli/ecommerce-data-pipeline-23MH1A05I0
cd ecommerce-data-pipeline-23MH1A05I0

Start PostgreSQL using Docker:
docker compose up -d

--------------------------------------------------

RUNNING THE DATA PIPELINE

Run the complete pipeline:
python scripts/orchestration/run_pipeline.py

This executes:
- Data generation
- CSV ingestion into staging schema
- Transformation to production schema
- Warehouse loading using star schema
- Analytics and reporting generation

--------------------------------------------------

RUNNING INDIVIDUAL STEPS

Data Generation:
python scripts/data_generation/generate_data.py

Ingestion:
python scripts/ingestion/ingest_to_staging.py

Transformation:
python scripts/transformation/staging_to_production.py

Warehouse Load:
python scripts/transformation/load_warehouse.py

--------------------------------------------------

TESTING

Run all tests:
pytest

Note:
Database-related tests require the Docker PostgreSQL service to be running.
Test coverage is maintained above 80 percent.

--------------------------------------------------

DATA MODEL

Staging Schema:
- Replica of raw CSV data
- Minimal validation
- Used for auditing and recovery

Production Schema (3NF):
- Removes redundancy
- Ensures referential integrity
- Enforces primary and foreign keys

Warehouse Schema (Star Schema):
Fact Table:
- fact_sales

Dimension Tables:
- dim_customer
- dim_product
- dim_date
- dim_payment

Slowly Changing Dimensions:
- Type 2 implemented
- Preserves historical changes

--------------------------------------------------

DASHBOARD ACCESS

The Power BI dashboard (.pbix) is available in:
dashboards/powerbi/

To view:
1. Open Power BI Desktop
2. Open the pbix file
3. Click Refresh

--------------------------------------------------

DASHBOARD PAGES

Page 1: Executive Summary
- Revenue, orders, AOV, profit margin
- Monthly trends and category performance

Page 2: Product Analysis
- Product and category-wise revenue

Page 3: Customer Insights
- Customer segmentation and distribution

Page 4: Geographic and Trends
- State-wise revenue and time-based trends

--------------------------------------------------

METRIC DEFINITIONS

Total Revenue:
SUM(quantity × unit_price − discount)

Average Order Value:
Total Revenue / Total Orders

Profit Margin:
(Total Revenue − Cost) / Total Revenue × 100

Customer Lifetime Value:
Average Order Value × Purchase Frequency × Customer Lifespan

--------------------------------------------------

DECLARATION

I hereby declare that this project titled "E-Commerce Data Analytics Pipeline" is my original work completed independently for academic purposes.

Name: Lahari Sri Kotipalli
Roll Number: 23MH1A05I0
Email: laharisrikotipalli07@gmail.com
Submission Date: 25-12-2025
