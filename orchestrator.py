import subprocess
import sys
from prefect import flow, task


@task(name="Ingest MySQL to Postgres", retries=1)
def run_ingestion():
    """running script extraction main.py"""
    result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Ingestion failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@task(name="dbt Seed")
def run_dbt_seeds():
    """running dbt seed to create reference tables"""
    result = subprocess.run(
        ["dbt", "seed"], cwd="./transform", capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt seed failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@task(name="dbt Run")
def run_dbt_models():
    """running dbt run"""
    result = subprocess.run(
        ["dbt", "run"], cwd="./transform", capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    print(result.stdout)


@task(name="dbt Test")
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
    main_pipeline()