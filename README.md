# AY22/23 Semester 2 IS3107 Group 6: EZ Property
EZ Property is your one-stop shop to figuring out the best places to buy your new property in Singapore.

## File Structure
The project is structured by business functions.
```
./
├── README.md
├── requirements.txt            # pip libraries needed
├── env
├── db
│   ├── __init__.py                # Main DB script
│   ├── data_loader.py          # Initialises database
│   ├── warehouse
│   │   ├── mysql_connector.py  # Connects to localhost:3306
│   │   └── schemas
│   │       ├── property_transaction.py
│   │       ├── hdb_info.py
│   │       └── etc. 
│   └── lake
│       └──mongo_connector.py   # Connects to localhost:27017
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
```
# Create environment and download packages
> sed -i 's/\r$//' ./build.sh
> ./build.sh

# Enter environment
> source env/bin/activate

# Start Airflow
> airflow webserver --port 8080 -D
> airflow scheduler -D

# Initialises database
> python data_loader.py

# Run data injection
> airflow dags init_load 2023-XX-YY

# Run the frontend
> cd app && npm start
```