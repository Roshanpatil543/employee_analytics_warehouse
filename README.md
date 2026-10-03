# Enterprise Employee Analytics & Data Warehouse System

This project implements an end-to-end employee analytics solution spanning OLTP data management, dimensional warehouse modeling, ETL logic, and a Streamlit dashboard. It is built to satisfy the design and architecture requirements for a cloud-ready employee analytics platform.

## Project Goals

- Track employee onboarding, project assignments, and review history.
- Store transactional data in a normalized OLTP schema.
- Maintain historical employee dimension data using SCD Type 2 logic.
- Load and analyze aggregated data through a star-schema warehouse.
- Present KPI dashboards in a Streamlit web app.
- Provide modular Python classes and SQL scripts for maintainability.

## Architecture Overview

- OLTP layer: employee, project, department, assignment, and review data.
- Warehouse layer: fact and dimension tables with surrogate keys.
- ETL layer: SQL + Python process to extract, transform, and load data.
- Streamlit app: onboarding workflow and analytics dashboard.

## Repository Structure

```text
employee_analytics_warehouse/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db_manager.py
│   ├── models.py
│   ├── managers.py
│   ├── data_synthesizer.py
│   ├── etl_pipeline.py
│   └── streamlit_app.py
├── sql/
│   ├── oltp_schema.sql
│   ├── warehouse_schema.sql
│   ├── etl_scripts.sql
│   └── analysis_queries.sql
├── docs/
│   ├── er_diagram.mmd
│   └── dimensional_model.mmd
├── .gitignore
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

## Technologies

- Python 3
- MySQL Workbench / MySQL Server
- Pandas + Faker
- Streamlit + Plotly
- SQL Stored Procedures, CTEs, and Window Functions

## Local Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure MySQL and set environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=yourpassword
export DB_NAME=employee_analytics
```

4. Apply the SQL schema files in MySQL:

```sql
SOURCE sql/oltp_schema.sql;
SOURCE sql/warehouse_schema.sql;
SOURCE sql/etl_scripts.sql;
```

5. Run the data synthesizer:

```bash
python -m app.data_synthesizer --rows 100000 --historical-fraction 0.30
```

6. Launch the app:

```bash
streamlit run app/streamlit_app.py
```

## Data Synthesis Logic

The synthesizer downloads or reads a base employee dataset, expands it to 100,000+ rows, and simulates historical changes for a subset of employees so the HR dimension can support SCD Type 2. The generated history includes:

- department changes
- role promotions
- salary revisions
- start/end effective dates
- current flag tracking

## SCD Type 2 Handling

Employee dimension rows are treated as history records. Each version of an employee is valid between a start date and end date, with the current row marked as active.

## Notes

- The project is structured for local development and cloud deployment with Streamlit Community Cloud.
- Database credentials should be stored securely outside the repo.
- The Streamlit app includes graceful fallback behavior when the database is not reachable.

## Future Extensions

- Add secure authentication for HR and executive views.
- Add automated ETL jobs with cron or scheduler.
- Migrate to cloud database services such as MySQL RDS or PlanetScale.
