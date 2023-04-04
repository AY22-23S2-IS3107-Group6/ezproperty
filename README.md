# AY22/23 Semester 2 IS3107 Group 6: EZ Property

EZ Property is your one-stop shop to figuring out the best places to buy your new property in Singapore.

## File Structure

The project is structured by business functions.

```
./
├── README.md
├── env
├── db
│   ├── __init__.py             # Main DB script
│   ├── warehouse
│   │   ├── __init__.py
│   │   ├── mysql_connector.py  # Connects to localhost:3306
│   │   └── schemas
│   │       ├── __init__.py
│   │       ├── main.py         # Schemas for main database
│   │       ├── ref.py          # Schemas for reference database
│   │       └── amn.py          # Schemas for amenities database
│   └── lake
│       ├── __init__.py
│       └── mongo_connector.py   # Connects to localhost:27017
├── airflow
│   ├── index.py
│   ├── data_gov_api.py
│   ├── ura_api.py
│   └── external_api.py
├── app
├── notebooks
├── dataviz
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
> virtualenv env

# Enter environment
> source env/bin/activate # macOS/linux
> .\env\Scripts\activate # windows
> pip install -r requirements.txt

# You may have to run this if mysqlclient refuses to download during pip install
> sudo apt-get install python-dev default-libmysqlclient-dev
> sudo apt-get install python3-dev

# Run ETL file
> python3 -m db.etl.[etl file name]

# Start Airflow
> airflow webserver --port 8080 -D
> airflow scheduler -D

# Run data injection
> airflow dags init_load 2023-XX-YY

# Run the backend
> export FLASK_APP=db/app
> export FLASK_ENV=development
> flask run

# Run the frontend
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
