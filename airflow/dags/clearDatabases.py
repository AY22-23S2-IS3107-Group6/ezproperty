import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from db import DataLake, DataWarehouse

default_args = {
    'owner': 'airflow',
}

with DAG(
    'clearDatabases',
    default_args=default_args,
    description='Clears DB and re-init',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['is3107g6'],
) as dag:

    dag.doc_md = __doc__

    def resetDataLake(**kwargs):
        DataLake(True)

    def resetDataWarehouse(**kwargs):
        DataWarehouse(True, True)
    
    resetDataLake = PythonOperator(task_id="resetDataLake", python_callable=resetDataLake)
    resetDataWarehouse = PythonOperator(task_id="resetDataWarehouse", python_callable=resetDataWarehouse)
    resetDataLake >> resetDataWarehouse