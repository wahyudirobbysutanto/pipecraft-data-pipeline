# PipeCraft: End-to-End Local Data Pipeline & Analytics Platform

**PipeCraft** is a complete, production-grade local Data Engineering pipeline. It extracts raw transactional data from an OLTP database (MySQL), loads it into a Data Warehouse (PostgreSQL), transforms raw schemas into clean analytical data marts using **dbt**, orchestrates workflow dependencies with **Prefect 3.x**, and serves executive insights via an interactive **Metabase** dashboard.

The project is fully dockerized with a decoupled architecture—separating persistent database infrastructure from containerized batch processing jobs via custom Docker networks.

---

## 📸 Executive Dashboard Showcase

Below is the **Executive Sales Dashboard** built on Metabase, consuming directly from the dbt-modeled `analytics` schema in PostgreSQL (`bizpulse_dwh`).

![Executive Sales Dashboard](Image/Dashboard.JPG)

---

## 🏗️ Architecture & Data Flow

```
[ MySQL Container (3307:3306) ]
       │
       ▼  (Docker Network: pipecraft_net)
[ Python Pipeline Container (pipecraft_pipeline) ]
       │  (Extract & Load via SQLAlchemy / PyMySQL / Psycopg2)
       ▼
[ PostgreSQL Container (5433:5432 - bizpulse_dwh) ]
       │
       ▼  (dbt-core Transformations, Seeds, & Tests)
[ PostgreSQL (bizpulse_dwh - analytics schema) ]
       ├── fct_product_performance
       └── fct_payment_summary
       │
       ▼  (Metabase BI Dashboard)
[ Executive Sales Dashboard ]
```

**Orchestration & Containerization Layer:**
- **Infrastructure Isolation:** MySQL (`pipecraft_mysql`) and PostgreSQL (`pipecraft_postgres`) run as persistent services.
- **Batch Pipeline Execution:** Python ingestion runs in a dedicated container (`pipecraft_pipeline`) and terminates upon completion.
- **Workflow Orchestration:** Prefect 3.x (`orchestrator.py`) handles interval-based scheduling, dependency management, and error handling.

---

## 🛠️ Tech Stack

* **Containerization & Networking:** Docker, Docker Compose, External Bridge Networks (`pipecraft_net`)
* **Source Database (OLTP):** MySQL 8.0 Container
* **Data Warehouse (OLAP):** PostgreSQL 15 Container (`bizpulse_dwh`)
* **Data Ingestion:** Python 3.10 (`pandas`, `sqlalchemy`, `pymysql`, `psycopg2-binary`, `python-dotenv`)
* **Data Transformation & Modeling:** `dbt-core` v1.12+ (Postgres Adapter)
* **Workflow Orchestration:** `prefect` v3.8+
* **Business Intelligence:** Metabase Standalone (Java 21 JDK Runtime)

---

## 📊 Analytical Data Marts (dbt Models)

The transformation layer produces clean, aggregated data marts in the `analytics` schema:

1. **`analytics.fct_product_performance`**
   * **Purpose:** Measures total sales revenue and units sold per product category.
   * **Key Metrics:** `total_revenue_generated`, `total_units_sold`.
2. **`analytics.fct_payment_summary`**
   * **Purpose:** Breakdown of revenue distribution across payment channels.
   * **Key Metrics:** `grand_total_revenue`, segmented by `payment_method` (QRIS, Transfer Bank, Kartu Kredit, Cash).

---

## 🚀 How to Run

### Option A: Fully Containerized with Docker (Recommended)

#### 1. Prerequisite
Ensure Docker Desktop or Docker Engine with Docker Compose plugin is installed and running.

#### 2. Create Docker External Network
Run this once to establish a shared communication channel between containers:
```powershell
docker network create pipecraft_net
```

#### 3. Spin Up Persistent Database Infrastructure
Starts MySQL (`port 3307`) and PostgreSQL (`port 5433`) with initial database schemas loaded from `Data/`:
```powershell
docker compose -f docker-compose.db.yml up -d
```

#### 4. Build and Run Data Pipeline Container
Builds the Python Docker image and executes the data ingestion pipeline:
```powershell
docker compose -f docker-compose.app.yml up --build
```

#### 5. Verify Database State with DBeaver / GUI Client
* **MySQL Source:** Host `localhost`, Port `3307`, User `root`, Pass `abc123!@#`, DB `bizpulse_db`
* **PostgreSQL DWH:** Host `localhost`, Port `5433`, User `postgres`, Pass `abc123!@#`, DB `bizpulse_dwh`

---

### Option B: Local OS Execution (Python Virtual Environment)

#### 1. Environment Setup
Clone the repository and prepare `.env`:
```powershell
copy .env.example .env
```

Ensure `.env` matches your local database ports:
```env
MYSQLDB_host=127.0.0.1
MYSQLDB_port=3307
MYSQLDB_user=root
MYSQLDB_PASSWORD="YOUR_MYSQLDB_PASSWORD"
MYSQLDB_DATABASE=bizpulse_db

POSTGRES_host=127.0.0.1
POSTGRES_port=5433
POSTGRES_user=postgres
POSTGRES_PASSWORD="YOUR_POSTGRESQL_PASSWORD"
POSTGRES_DATABASE=bizpulse_dwh
```

#### 2. Install Python Dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

#### 3. Run Pipeline Steps

* **Run via Prefect Orchestrator (Full DAG):**
  ```powershell
  python orchestrator.py
  ```

* **Run Step-by-Step Manual Pipeline:**
  1. **Ingest Raw Data:**
     ```powershell
     python main.py
     ```
  2. **Transform Data with dbt:**
     ```powershell
     cd transform
     dbt seed
     dbt run
     dbt test
     ```

---

### 🖥️ Launch Metabase BI Server
From the root directory:
```powershell
cd bi
java -jar metabase.jar
```
Access the dashboard in your browser at `http://localhost:3000`.

---

## 🧹 Docker Cleanup Commands

* **Stop Pipeline Container:**
  ```powershell
  docker compose -f docker-compose.app.yml down
  ```
* **Stop Databases & Reset Volumes (Fresh Start):**
  ```powershell
  docker compose -f docker-compose.db.yml down -v
  ```

---

## 📂 Project Structure

```
pipecraft-data-pipeline/
├── bi/
│   └── metabase.jar          # Metabase standalone runner (gitignored)
├── Data/
│   ├── mysql_initial.sql     # Initial MySQL tables and sample data
│   └── initial.sql           # PostgreSQL schema initialization (staging & analytics)
├── Image/
│   └── Dashboard.JPG         # Metabase Executive Dashboard preview
├── transform/                # dbt transformation project
│   ├── models/               # Staging & Analytics dbt models
│   ├── seeds/                # Reference seed CSVs
│   ├── dbt_project.yml       # dbt configurations
│   └── profiles.yml          # dbt connection profiles
├── .dockerignore             # Excluded files for Docker build context
├── .env.example              # Environment variables template
├── .gitignore                # Excluded binary files & secrets
├── docker-compose.app.yml    # Pipeline batch application compose
├── docker-compose.db.yml     # Persistent database infrastructure compose
├── Dockerfile                # Python pipeline image specification
├── main.py                   # Custom Python ingestion script
├── orchestrator.py           # Prefect DAG flow & scheduler
└── requirements.txt          # Python dependencies
```