import json
import requests
from datetime import datetime
from textwrap import dedent
from airflow import DAG
# from airflow.operators.python import PythonOperator

# from ...db.etl.carparkPublic import extract

default_args = {
    'owner': 'airflow',
}

with DAG(
    'is3107_project_init_load', 
    default_args=default_args, 
    description='IS3107 Group Project', 
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    dag.doc_md = __doc__
    def carpark_public_etl(**kwargs):
        print("First run")
        # extract()
        # for future reference # ti.xcom_push('latestBlock', x_dict.get("result"))
    def carpark_season_etl(**kwargs):
        print("Second run")

    # carpark_public_etl_task = PythonOperator(task_id='carpark_public_etl', python_callable=carpark_public_etl,)
    # carpark_season_etl_task = PythonOperator(task_id='carpark_season_etl', python_callable=carpark_season_etl,)

    # carpark_public_etl_task >> carpark_season_etl_task