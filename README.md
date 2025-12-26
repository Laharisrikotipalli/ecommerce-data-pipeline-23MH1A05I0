Below is **ONE SINGLE CONTINUOUS BLOCK**.
👉 **Click once → Select all → Copy → Paste**
It includes **architecture description**, **architecture image from repo**, and **your OneDrive Power BI link**.
Nothing extra before or after.

---

# E-COMMERCE DATA ANALYTICS PIPELINE

## Project Overview

This project implements an end-to-end E-Commerce Data Analytics Pipeline that generates synthetic data, ingests it into PostgreSQL, processes it across staging, production, and warehouse layers, and visualizes insights using Power BI. The pipeline follows modern data engineering best practices including data generation, ingestion, transformation, orchestration, automated testing, containerization, and BI visualization.

## Architecture Overview

The pipeline follows a three-layer architecture designed for scalability, data quality, and analytics performance.

* **Staging Layer** – Stores raw ingested CSV data with minimal validation for auditing and recovery
* **Production Layer** – Normalized (3NF) schema ensuring data integrity and consistency
* **Warehouse Layer** – Star Schema optimized for analytical queries and BI dashboards

The warehouse uses a fact table and multiple dimension tables to support fast aggregations and reporting.

### Architecture Diagram

The architecture diagram is included in this repository at the following path:

docs/image/architecture_overview.png

![Architecture Overview](docs/image/architecture_overview.png)

## Project Structure

The project is organized into configuration files, dashboards, raw and processed data folders, pipeline scripts, SQL files, tests, Docker configuration, and documentation. Each directory follows a clear responsibility-based structure to ensure maintainability and scalability.

## Code Organization

Data generation creates synthetic datasets. Ingestion loads raw CSV data into staging tables. Transformation moves data into production and warehouse schemas. Quality checks validate data accuracy and integrity. Orchestration runs the entire pipeline end-to-end. Monitoring tracks execution status and logs. SQL scripts define schemas and analytical queries. Tests ensure correctness and reliability.

## Configuration

Database credentials are managed using environment variables. Configuration values are centralized in config/config.yaml. Docker provides a consistent and reproducible execution environment.

## Prerequisites

Python 3.9 or higher, Docker and Docker Compose, and Power BI Desktop.

## Installation and Setup

Clone the repository, navigate into the project directory, and start PostgreSQL using Docker Compose.

## Running the Data Pipeline

Run the pipeline orchestrator script to execute data generation, ingestion into staging, transformation to production, warehouse loading using a star schema, and analytics generation.

## Running Individual Steps

Each stage of the pipeline can be executed independently, including data generation, ingestion, transformation, and warehouse loading.

## Testing

All tests can be executed using pytest. Database-related tests require the Docker PostgreSQL service to be running. Test coverage is maintained above 80 percent.

## Data Model

The staging schema mirrors raw CSV data with minimal validation. The production schema follows third normal form to reduce redundancy and enforce referential integrity. The warehouse schema follows a Star Schema with `fact_sales` as the fact table and customer, product, date, and payment dimensions. Slowly Changing Dimension Type 2 is implemented to preserve historical changes.

## Dashboard Access

The Power BI dashboard is available in two ways:

* **Local PBIX file:**
  dashboards/powerbi/

* **OneDrive Download Link:**
  [https://adityagroup-my.sharepoint.com/:u:/g/personal/23mh1a05i0_acoe_edu_in/IQBv4ElDQPvbRa8R_ere1HYyAVVpCkm19IaIB-JLUZA0G6g?e=j8mJbj](https://adityagroup-my.sharepoint.com/:u:/g/personal/23mh1a05i0_acoe_edu_in/IQBv4ElDQPvbRa8R_ere1HYyAVVpCkm19IaIB-JLUZA0G6g?e=j8mJbj)

To view the dashboard:

1. Open Power BI Desktop
2. Open the PBIX file
3. Click **Refresh** to load the latest data

## Dashboard Pages

The Executive Summary page provides high-level metrics such as revenue, orders, average order value, profit margin, and trends. The Product Analysis page shows product and category performance. The Customer Insights page presents customer segmentation and distribution. The Geographic and Trends page displays state-wise revenue and time-based trends.

## Metric Definitions

Total Revenue is calculated as quantity multiplied by unit price minus discount. Average Order Value is calculated as total revenue divided by total orders. Profit Margin is calculated as profit divided by total revenue. Customer Lifetime Value is derived from average order value, purchase frequency, and customer lifespan.

## Declaration

I hereby declare that this project titled **E-Commerce Data Analytics Pipeline** is my original work completed independently for academic purposes.

Name: Lahari Sri Kotipalli
Roll Number: 23MH1A05I0
Email: [laharisrikotipalli07@gmail.com](mailto:laharisrikotipalli07@gmail.com)
Submission Date: 25-12-2025
