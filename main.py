import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import urllib.parse


def main():
    load_dotenv()

    mysql_user = urllib.parse.quote_plus(os.getenv('MYSQLDB_user'))
    mysql_password = urllib.parse.quote_plus(os.getenv('MYSQLDB_PASSWORD'))
    mysql_database = urllib.parse.quote_plus(os.getenv('MYSQLDB_DATABASE'))
    
    postgres_user = urllib.parse.quote_plus(os.getenv('POSTGRES_user'))
    postgres_password = urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD'))
    postgres_database = urllib.parse.quote_plus(os.getenv('POSTGRES_DATABASE'))

    # 1. Connect to MySQL (using the PyMySQL driver)
    mysql_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{os.getenv('MYSQLDB_host')}:{os.getenv('MYSQLDB_port')}/{mysql_database}"
    mysql_engine = create_engine(mysql_url)

    # 2. Connect to PostgreSQL (using the psycopg2 driver)
    postgres_url = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{os.getenv('POSTGRES_host')}:{os.getenv('POSTGRES_port')}/{postgres_database}"
    postgres_engine = create_engine(postgres_url)

    # 3. Get all table names from MySQL using SQLAlchemy Inspector
    inspector = inspect(mysql_engine)
    mysql_tables = inspector.get_table_names()
    print("MySQL Tables:", mysql_tables)

    for table in mysql_tables:
        columns = inspector.get_columns(table)
        print(f"Columns in {table}: {[column['name'] for column in columns]}")

        try:
            # Read data from MySQL table into a DataFrame
            with mysql_engine.connect() as conn:
                df = pd.read_sql(text(f"SELECT * FROM {table}"), con=conn)

            # Write DataFrame to PostgreSQL table
            # if_exists='replace' creates the table if missing or overwrites it.
            # Use if_exists='append' if you want to keep existing destination records.
            df.to_sql(
                name=f'{table}', 
                schema="staging", 
                con=postgres_engine, 
                if_exists='replace', 
                index=False,
                chunksize=1000,
                method='multi'
            )
            print(f"Data from MySQL table '{table}' has been copied to PostgreSQL.")
        except Exception as e:
            print(f"Error processing table '{table}': {e}")

    

if __name__ == "__main__":
    main()