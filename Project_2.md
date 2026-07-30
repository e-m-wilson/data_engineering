# Project 2

## Project Description

Design and implement an end-to-end modern data platform that ingests streaming data, processes and orchestrates data pipelines, stores curated datasets in Snowflake, and delivers business insights through interactive Power BI dashboards.

This capstone project should integrate all technologies covered during training and simulate a real-world enterprise data engineering and analytics solution.

---

## Objective / Tools Used

### Objectives

- Build a data pipeline that incorporates both batch and streaming data processing.
- Use Kafka to ingest and distribute real-time events.
- Process and transform data using PySpark.
- Orchestrate workflows using Airflow.
- Store raw, curated, and analytics-ready datasets in Snowflake.
- Create business intelligence dashboards in Power BI.
- Implement monitoring, validation, and error-handling mechanisms.
- Demonstrate collaboration through team-based development practices.

### Tools Used

- Python
- PySpark
- Apache Kafka
- Apache Airflow
- Docker
- Snowflake
- SQL
- Power BI
- Git/GitHub
- Jupyter Notebook or VS Code

---

## Project Timeline

**Weeks During Training:** 3–6

**Project Type:** Group Project

---

## Sample Business Scenario

An online retail company wants to monitor customer purchases, website activity, and product performance in near real time.

Streaming transaction data is captured through Kafka, processed and enriched using PySpark, orchestrated by Airflow, stored in Snowflake, and visualized through executive and operational dashboards in Power BI.

---

# Requirements

## 1. Data Ingestion

- Generate or source streaming event data:
  - Orders
  - Website clicks
  - Transactions
  - IoT readings
  - Other event-based data

- Publish events to Kafka topics.
- Implement Kafka producers and consumers.
- Capture and store raw data for auditing purposes.

---

## 2. Data Processing

Use PySpark to:

- Clean and validate incoming data.
- Handle missing or malformed records.
- Create calculated business metrics.
- Aggregate data.

---

## 3. Workflow Orchestration

Build Airflow DAGs to:

- Trigger ingestion processes.
- Execute transformation jobs.
- Load data into Snowflake.
- Perform data quality checks.
- Generate pipeline execution logs.

---

## 4. Data Warehousing

- Design a Snowflake data model using:
  - Fact tables
  - Dimension tables

- Create environments for:
  - Raw data
  - Staging data
  - Curated data

- Load transformed datasets into Snowflake.
- Implement SQL-based validation and analytical queries.

---

## 5. Business Intelligence

Develop Power BI dashboards that include:

### Executive KPI Summary

- Key business performance indicators.

### Sales and Revenue Trends

- Revenue analysis over time.
- Sales performance tracking.

### Customer Insights

- Customer behavior and purchasing patterns.

### Product Performance Analysis

- Product-level sales and performance metrics.

### Operational Monitoring Metrics

- Pipeline and operational health insights.

Include:

- Interactive filters
- Drill-down capabilities
- Visual storytelling elements

---

## 6. Data Quality & Monitoring

- Validate source-to-target record counts.
- Identify and log failed records.
- Create basic monitoring and audit reports.

---

## 7. Team Collaboration

- Use Git/GitHub for source control.
- Assign clear team responsibilities:
  - Data Ingestion
  - Processing
  - Orchestration
  - Analytics
  - Documentation

- Maintain:
  - Project documentation
  - Meeting notes

---

# Deliverables

- Source code repository
- Kafka producer and consumer applications
- PySpark processing scripts
- Airflow DAGs
- Snowflake DDL, DML, and SQL scripts
- Power BI dashboard files
- Architecture diagram
- Technical documentation
- Final team presentation and demonstration

---

# Outcome

By completing this capstone project, learners will demonstrate the ability to design, build, orchestrate, and monitor a complete modern data platform.

Teams will gain practical experience with:

- Streaming data pipelines
- Workflow automation
- Cloud data warehousing
- Business intelligence reporting
- Collaborative software development practices

Learners will apply all technologies covered throughout the six-week training program.