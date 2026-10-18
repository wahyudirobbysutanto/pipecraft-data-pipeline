import os
import logging
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
import pandas as pd

# Configuring logging to log messages to both terminal and pipeline.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def main():
    load_dotenv()
    logging.info("Start process ingestion data from MySQL to PostgreSQL...")

    # Protect Database Connection
    try:
        mysql_user = urllib.parse.quote_plus(os.getenv('MYSQLDB_user', ''))
        mysql_password = urllib.parse.quote_plus(os.getenv('MYSQLDB_PASSWORD', ''))
        mysql_database = urllib.parse.quote_plus(os.getenv('MYSQLDB_DATABASE', ''))
        
        postgres_user = urllib.parse.quote_plus(os.getenv('POSTGRES_user', ''))
        postgres_password = urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD', ''))
        postgres_database = urllib.parse.quote_plus(os.getenv('POSTGRES_DATABASE', ''))

        # Connect to MySQL (using PyMySQL driver)
        mysql_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{os.getenv('MYSQLDB_host')}:{os.getenv('MYSQLDB_port')}/{mysql_database}"
        mysql_engine = create_engine(mysql_url)

        # Connect to PostgreSQL (using psycopg2 driver)
        postgres_url = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{os.getenv('POSTGRES_host')}:{os.getenv('POSTGRES_port')}/{postgres_database}"
        postgres_engine = create_engine(postgres_url)

        # Test connection to both databases
        with mysql_engine.connect() as conn_m, postgres_engine.connect() as conn_p:
            pass
        logging.info("Connection to MySQL and PostgreSQL established successfully.")
    except Exception as e:  
        logging.error(f"Error connecting to databases: {e}")
        return

    # Extract and ingest data from MySQL to PostgreSQL 
    try:
        inspector = inspect(mysql_engine)
        mysql_tables = inspector.get_table_names()
        logging.info(f"MySQL Tables detected: {mysql_tables}")

        for table in mysql_tables:
            columns = inspector.get_columns(table)
            logging.info(f"Columns in {table}: {[column['name'] for column in columns]}")

            try:
                # Read data from MySQL table into a DataFrame
                with mysql_engine.connect() as conn:
                    df = pd.read_sql(text(f"SELECT * FROM {table}"), con=conn)

                # Write DataFrame to PostgreSQL table
                df.to_sql(
                    name=table, 
                    schema="staging", 
                    con=postgres_engine, 
                    if_exists='replace', 
                    index=False,
                    chunksize=1000,
                    method='multi'
                )
                logging.info(f"Data from MySQL table '{table}' ({len(df)} rows) copied to PostgreSQL staging.")
            except Exception as e:
                logging.error(f"Error processing table '{table}': {e}")

    except Exception as e:
        logging.error(f"Error during data extraction and ingestion: {e}")

    logging.info("Data ingestion process completed successfully.")

if __name__ == "__main__":
    main()