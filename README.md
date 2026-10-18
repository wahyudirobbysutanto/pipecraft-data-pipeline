# PipeCraft End-to-End Data Pipeline

An end-to-end Data Engineering pipeline extracting transactional data from MySQL (OLTP) to PostgreSQL (Data Warehouse) staging, transformed via dbt, and orchestrated locally.

## Architecture
MySQL (OLTP) -> Python EL Script -> PostgreSQL (Staging) -> dbt Core (Analytics)

## Tech Stack
- Database: MySQL, PostgreSQL
- Ingestion: Python (SQLAlchemy, Pandas, PyMySQL, Psycopg2)
- Transformation: dbt-core (Analytics layer)

## How to Run
1. **Clone Repository**
2. **Environment Setup:**
   Copy .env.example to .env and fill in your database credentials:
   ```
   copy .env.example .env
   ```
3. **Execute Engine:**
   ```cmd
   python main.py
   ```