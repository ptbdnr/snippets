import os
import sys
import pandas as pd
import sqlalchemy

HOST = 'foo.host.com'
PORT = 3306
DB_NAME = 'db'
TABLE_NAME = 'tbl'
USERNAME = 'joe'
PASSWORD = 'pass'
HOST_TYPE = 'MySQL'  # or 'PostgreSQL'

INPUT_FILEPATH = 'test.csv'

print(f"Python version: {sys.version}")
print(f"pandas package version: {pd.__version__}")
print(f"sqlalchemy package version: {sqlalchemy.__version__}")

# read input
df = pd.read_csv(filepath_or_buffer=INPUT_FILEPATH)

print(df.info(verbose=True))
print('============================')
print(df.describe())
print('============================')
print(df.head())

## Insert to MySQL
if HOST_TYPE.lower().strip() == 'mysql':
    print(f"Host type: {HOST_TYPE}")

    import mysql.connector  # pip install mysql-connector-python
    print(f"mysql.connector package version: {mysql.connector.__version__}")

    # connect to database
    url = sqlalchemy.engine.url.URL.create(
        drivername='mysql+mysqlconnector',
        host=HOST, port=PORT, database=DB_NAME,
        username=USERNAME, password=PASSWORD)
    engine = sqlalchemy.create_engine(
        url,
        pool_recycle=30 * 60,  # connection allowed for 30 minute,
        pool_size=5,  # 5 simultaneous connections
        echo=True)

    # insert data to database
    df.to_sql(name=TABLE_NAME, con=engine, schema=DB_NAME, if_exists='append', index=False, chunksize=1000)

## Insert to PostgreSQL
if HOST_TYPE.lower().strip() == 'postgresql':
    print(f"Host type: {HOST_TYPE}")
    print(f"UNTESTED")

    import pg8000
    print(f"pg8000 package version: {pg8000.__version__}")

    # connect to database
    url = sqlalchemy.engine.url.URL.create(
        drivername='postgresql+pg8000',
        host=HOST, port=PORT, database=DB_NAME,
        username=USERNAME, password=PASSWORD)
    engine = sqlalchemy.create_engine(
        url,
        pool_recycle=30 * 60,  # connection allowed for 30 minute,
        pool_size=5,  # 5 simultaneous connections
        echo=True)

    # insert data to database
    df.to_sql(name=TABLE_NAME, con=engine.connect(), schema=DB_NAME, if_exists='append', index=False, chunksize=1000)
