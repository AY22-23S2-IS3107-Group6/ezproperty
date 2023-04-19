# AY22/23 Semester 2 IS3107 Group 6: EZ Property

EZ Property is your one-stop shop to figuring out the best places to buy your new property in Singapore.

## File Structure

The project is structured by business functions.

```
./
├── README.md
├── env
├── venv                        # If you need two environments
├── db
│   ├── __init__.py             # Main DB script
│   ├── warehouse
│   │   ├── __init__.py
│   │   ├── mysql_connector.py  # Connects to localhost:3306
│   │   └── schemas
│   │       ├── __init__.py
│   │       ├── main.py         # Schemas for main database
│   │       ├── ref.py          # Schemas for reference database
│   │       ├── amn.py          # Schemas for amenities database
│   │       └── test.py         # Schemas for test database
│   ├── lake
│   │   ├── __init__.py
│   │   └── mongo_connector.py  # Connects to localhost:27017
│   ├── etl
│   │   ├── carparkPublic.py
│   │   ├── ...
│   │   └── trainStation.py
│   ├── ml
│   │   ├── findCentroids.py
│   │   ├── assignDistrict.py
│   │   ├── predictPrice.py
│   │   └── predictPrice2.ipynb
│   ├── app.py                  # Flask app
│   └── utils.py                # Utility functions
├── airflow/dags                # DAG bag folder
│   ├── carparkPublic.py
│   ├── ...
│   └── trainstation.py 
├── app
└── etc.
```

## Deploy and Building the project

### Dependencies

1. Ensure MySQL database service is running on `localhost:3306`
2. Ensure MongoDB database is running on `localhost:27017`

### Commands

Run this on WSL or bash

```bash
# Create environment and download packages
(base) virtualenv env

# Enter environment
(base) source env/bin/activate # macOS/linux
(env) .\env\Scripts\activate # windows
(env) pip install -r requirements.txt
(env) pip install ... # manual installation for failing libraries

# You may have to run this if mysqlclient refuses to download during pip install
(env) sudo apt-get install python-dev default-libmysqlclient-dev
(env) sudo apt-get install python3-dev gcc

# Run ETL file
(env) python -m db.etl.[etl file name]
(env) python -m db.etl.primarySchool.py # has to be run on your native os terminal

# Start Airflow
<Terminal 1>
(env) airflow webserver --port 8080

<Terminal 2>
(env) airflow scheduler

# Run the backend
# for macOS Monterey/Ventura, turn off Airplay Receiver in System Settings
<Terminal 3>
(env) export FLASK_APP=db/app
(env) export FLASK_ENV=development
(env) flask run

# Run the frontend
<Terminal 4>
> cd app
> npm install
> npm start
```

## Using the Data Lake and Data Warehouse

To insert documents without a specified schema and query from it, import the data lake

```python
from ..db import DataLake

# Transform data to list of objects
data = [{ "col1": "row1", "col2": "row2"}]

# Insert data
db = DataLake()
db.insert_to_schema("Collection Name", data)

# Query data using aggregate
result = db.query("Collection Name", [
    {"$match": {"col1": "row1"}},
    {"$project": {"_id": 0, "col2": 1}}
])

for x in result:
    print(x)

# Out[1]: {'col2': 'row2'}
```

To insert documents with a specified schema and query from it, import the data warehouse

```python
from ..db import DataWarehouse

# Transform data to list of tuples arranged by the column definition
data = [{ "col1": "row1", "col2": "row2"}]
data = list(map(lambda x: tuple(x.values()), data))

# Insert data
db = DataWarehouse()
db.insert_to_schema("subschema__Collection", data)

# Query data using SQL
result = db.query('''
    SELECT * FROM subschema__Collection
''')

for x in result:
    print(x)

# Out[1]: {'col1': 'row1', 'col2': 'row2'}
```

## Using Airflow

Change the airflow config
```python
> airflow.cfg

# How long before timing out a python file import
dagbag_import_timeout = 60.0

# Number of seconds after which a DAG file is parsed. The DAG file is parsed every
# ``min_file_process_interval`` number of seconds. Updates to DAGs are reflected after
# this interval. Keeping this number low will increase CPU usage.
min_file_process_interval = 300

# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository. This path must be absolute.
dags_folder = /path/to/ezproperty/airflow/dags
```
Go to the webserver and filter by tag "is3107g6". Steps:
1. Run `clearDatabases` to initialise database in MySQL and MongoDB
2. Run `districtInfo` to initialise references
3. Run all other pipelines
4. If you run `primarySchool`, it may fail if you do not have `chromedriver`