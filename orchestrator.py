import subprocess
import sys
from prefect import flow, task


@task(name="Ingest MySQL to Postgres", retries=2, retry_delay_seconds=10)
def run_ingestion():
    """running extraction script main.py"""
    result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Ingestion failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@task(name="dbt Seed", retries=2, retry_delay_seconds=10)
def run_dbt_seeds():
    """running dbt seed to create reference tables"""
    result = subprocess.run(
        ["dbt", "seed"], cwd="./transform", capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt seed failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@task(name="dbt Run", retries=2, retry_delay_seconds=10)
def run_dbt_models():
    """running dbt run"""
    result = subprocess.run(
        ["dbt", "run"], cwd="./transform", capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@task(name="dbt Test", retries=1, retry_delay_seconds=5)
def run_dbt_tests():
    """running dbt test"""
    result = subprocess.run(
        ["dbt", "test"], cwd="./transform", capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@flow(name="PipeCraft End-to-End Pipeline")
def main_pipeline():
    # execution order (DAG)
    run_ingestion()
    run_dbt_seeds()
    run_dbt_models()
    run_dbt_tests()


if __name__ == "__main__":
    # main_pipeline()
    # option 1 : running the pipeline every 1 hour (3600 seconds)
    main_pipeline.serve(
        name="pipecraft-hourly-deployment",
        interval=60,
    )
    # Option 2: Running the pipeline automatically every day at 2 AM using a Cron expression
    # main_pipeline.serve(
    #     name="pipecraft-daily-deployment",
    #     cron="0 2 * * *",
    # )