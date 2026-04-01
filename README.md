# Data Pipelines with Airflow

## Project Overview

This project builds automated and monitored data pipelines using Apache Airflow for Sparkify, a music streaming company. The pipeline extracts JSON data from S3, loads it into Amazon Redshift, and runs data quality checks.

## Architecture
```
S3 (log-data + song-data)
        ↓
  Staging Tables (Redshift)
        ↓
  Fact Table: songplays
        ↓
  Dimension Tables: users, songs, artists, time
        ↓
  Data Quality Checks
```

## Custom Operators

- **StageToRedshiftOperator** — Copies JSON files from S3 to Redshift staging tables
- **LoadFactOperator** — Loads data into the songplays fact table
- **LoadDimensionOperator** — Loads data into dimension tables with truncate-insert or append mode
- **DataQualityOperator** — Runs SQL-based data quality checks

## Project Structure
```
airflow/
├── dags/
│   └── final_project.py
└── plugins/
    ├── operators/
    │   ├── stage_redshift.py
    │   ├── load_fact.py
    │   ├── load_dimension.py
    │   └── data_quality.py
    └── helpers/
        └── final_project_sql_statements.py
```

## Prerequisites

- Apache Airflow
- Amazon Redshift Serverless
- Amazon S3
- Airflow Connections:
  - `aws_credentials` — AWS Access Key ID and Secret Access Key
  - `redshift` — Redshift Serverless endpoint

## DAG Configuration

- Runs every hour
- No dependencies on past runs
- 3 retries on failure, every 5 minutes
- Catchup disabled