# E-Commerce Data Analytics Pipeline
## Project Overview

This project implements an end-to-end e-commerce data analytics pipeline that generates synthetic data, ingests it into ***PostgreSQL***, processes it through multiple schema layers, and visualizes insights using ***Power BI***.

The pipeline follows modern data engineering best practices including staging, production, warehouse modeling, orchestration, testing, and containerization.
***Architecture Layers***,
***Data Generation***,
***Data Ingestion***,
***Staging Schema***,
***Production Schema***,
***Warehouse Schema***,
***Analytics Layer***,
***BI Visualization Layer***,
***Orchestration & Monitoring***.

---

##  Architecture Overview

![Architecture Overview](docs/image/architecture_overview.png)

This diagram shows the high-level data flow from synthetic data generation to BI visualization.

---
## Project Structure
```
ecommerce-data-pipeline/
│
├── config/
│ └── config.yaml
│
├── dashboards/
│ ├── powerbi/
│ │ ├── ecommerce_analytics.pbix
│ │ └── ecommerce_analytics.pbit
│ └── screenshots/
│ ├── page1_executive.png
│ ├── page2_product.png
│ ├── page3_customer.png
│ └── page4_geographic.png
│
├── data/
│ ├── raw/
│ │ ├── customers.csv
│ │ ├── products.csv
│ │ ├── transactions.csv
│ │ └── transaction_items.csv
│ │
│ ├── staging/
│ │ └── ingestion_summary.json
│ │
│ └── processed/
│ ├── analytics/
│ │ ├── query1_top_products.csv
│ │ ├── query2_monthly_sales.csv
│ │ ├── query3_customer_segments.csv
│ │ ├── query4_category_sales.csv
│ │ ├── query5_payment_methods.csv
│ │ ├── query6_geography.csv
│ │ ├── query7_customers.csv
│ │ ├── query8_products.csv
│ │ ├── query9_daily_sales.csv
│ │ └── query10_discounts.csv
│ │
│ ├── monitoring_reports.json
│ ├── pipeline_execution.json
│ ├── transformation_summary.json
│ └── quality_reports/
│ └── quality_report.json
│
├── scripts/
│ ├── data_generation/
│ │ └── generate_data.py
│ │
│ ├── ingestion/
│ │ └── ingest_to_staging.py
│ │
│ ├── transformation/
│ │ ├── cleanup_old_data.py
│ │ ├── load_dim_date.py
│ │ ├── load_warehouse.py
│ │ └── staging_to_production.py
│ │
│ ├── database/
│ │ └── warehouse_setup.sql
│ │
│ ├── monitoring/
│ │ └── pipeline_monitor.py
│ │
│ ├── quality_checks/
│ │ └── validate_data.py
│ │
│ ├── pipeline_orchestrator.py
│ └── scheduler.py
│
├── sql/
│ ├── ddl/
│ │ ├── create_staging_tables.sql
│ │ ├── create_production_tables.sql
│ │ └── create_warehouse_tables.sql
│ │
│ └── queries/
│ ├── analytical_queries.sql
│ ├── data_quality_checks.sql
│ ├── monitoring_queries.sql
│ ├── load_dim_date.sql
│ └── load_fact_sales.sql
│
├── tests/
│ ├── test_data_generation.py
│ ├── test_ingestion.py
│ ├── test_quality_checks.py
│ ├── test_transformation.py
│ └── test_warehouse.py
│
├── docs/
│ ├── architecture.md
│ └── dashboard_guide.md
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── setup.sh
├── analytics_summary.json
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```
---
## Code Organization & Maintainability

The project follows a modular pipeline-based structure where each folder represents a single responsibility.

### Scripts Structure
- `data_generation/` – Synthetic data generation using Faker
- `ingestion/` – Loads raw CSV data into staging schema
- `transformation/` – Moves data from staging → production → warehouse
- `pipeline_orchestrator.py` – Executes the end-to-end pipeline

This modular design makes the system easy to debug, test, and extend.

---

## Configuration Options
- Database credentials are managed using environment variables
- Configuration values are centralized in `config/config.yaml`
- Scripts can be executed independently or via the orchestrator
- Docker ensures a consistent runtime environment

---

## Troubleshooting Guide

| Issue | Solution |
|-----|---------|
| Dashboard not updating | Refresh Power BI or rerun analytics scripts |
| Duplicate records | Verify staging truncation logic |
| Slow queries | Use warehouse aggregate tables |
| Database connection error | Check Docker PostgreSQL container status |

---
## Architecture Decisions (Why?)
***Why PostgreSQL?***

Open-source, reliable RDBMS

Strong support for analytical queries

Schema-based separation (staging / production / warehouse)

Excellent integration with Python & BI tools

***Why Star Schema for Warehouse?***

Optimized for analytics & BI queries

Faster aggregations

Simple joins (fact → dimensions)

Industry-standard dimensional modeling

***Why Layered Schemas?***

Staging → raw ingestion (audit & recovery)

Production → clean transactional truth

Warehouse → analytics-optimized structure

---
## Technical Maintainability
Setup Instructions 
Prerequisites
```
Python 3.9+

Docker & Docker Compose

PostgreSQL

Power BI Desktop / Tableau Public
```
***Installation***
```
git clone <repo-url>
cd ecommerce-data-pipeline
pip install -r requirements.txt
docker-compose up -d
```
---
## Data Model Documentation 
Staging Schema
Exact CSV replica
Minimal validation
Temporary storage
Purpose: raw data audit & recovery
***Production Schema (3NF)***
Why 3NF?
Eliminates redundancy
Ensures data integrity
Supports transactional correctness
***Features:***
Primary & foreign keys
Cleaned data
Referential integrity enforced
Warehouse Schema (Star Schema)
Structure
Fact Table: fact_sales
Dimensions:
dim_customer
dim_product
dim_date
dim_payment
Aggregates: precomputed KPIs

***Why Star Schema?***
BI-friendly
Faster joins
Easier metrics calculation
SCD (Slowly Changing Dimensions)
Type 2 implemented
Maintains historical changes (e.g., customer segment changes)
Ensures accurate historical analytics
Index Strategy
Indexes on:
Foreign keys
Date keys
Frequently filtered columns
Improves dashboard performance

## Dashboard & Analytics Documentation 
Dashboard Pages Explained
#### Page 1: Executive Summary
***Purpose: High-level business overview***
Visuals:
Total Revenue

Total Transactions

Average Order Value

Profit Margin

Monthly Revenue Trend

Top Categories

Payment Method Distribution

Geographic Sales Map

#### Page 2: Product Analysis

***Purpose: Product performance insights***

Insights:

Top 10 products contribute majority revenue

Electronics category has highest profit margin

Long-tail products generate lower volume

#### Page 3: Customer Insights

***Purpose: Customer behavior analysis***

Insights:

VIP customers contribute major revenue share

Customer retention trends visible

CLV comparison across segments

#### Page 4: Geographic & Trends

***Purpose: Location & time-based analysis***

Insights:

Top 5 states generate most revenue

Seasonal trends identified

Metric Definitions 
Total Revenue
SUM(quantity × unit_price − discount)

Average Order Value (AOV)
Total Revenue / Total Orders

Profit Margin
(Total Revenue − Cost) / Total Revenue × 100

Customer Lifetime Value (CLV)
CLV = Average Order Value × Purchase Frequency × Customer Lifespan

Payment method preferences vary by region

---
## Declaration

I hereby declare that this project titled “Power BI E-Commerce Analytics Dashboard” is an original work carried out by me.
The data, analysis, and dashboard visuals presented in this project are created for academic and learning purposes.
Any references or tools used have been duly acknowledged, and this work has not been submitted elsewhere for any other degree or certification.

***Name: Kotipalli Lahari Sri
Roll.No: 23MH1A05I0
Email: laharisrikotipalli07@gmail.com
Submission Date: 25-12-2025***

---
## Conclusion

This Power BI dashboard effectively transforms raw e-commerce data into meaningful visual insights, enabling better business understanding and decision-making.
