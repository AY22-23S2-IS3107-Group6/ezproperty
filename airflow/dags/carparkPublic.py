# import os
# import sys
# sys.path.insert(0, "../../")

# from pathlib import Path
# import sys
# sys.path.append(str(Path('../../').resolve()))

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
from db.etl.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from db.etl.carparkPublic import CarparkPublicPipeline

def log(pipeline: Pipeline, message: str):
    print(f"Airflow  | {pipeline.schema_name.ljust(26)} | {message}")

default_args = {
    'owner': 'airflow',
}

with DAG(
    'carparkPublic',
    default_args=default_args,
    description='Loads Public Carparks from URA API',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['amn'],
) as dag:

    dag.doc_md = __doc__

    def extract(**kwargs):
        log(CarparkPublicPipeline, "Extract start")
        ti = kwargs['ti']
        data = CarparkPublicPipeline.extract()
        ti.xcom_push('data', data)
        log(CarparkPublicPipeline, "Extract completed successfuly")

    def transform(**kwargs):
        log(CarparkPublicPipeline, "Transform Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='extract', key='data')
        transformed_data = CarparkPublicPipeline.transform(data)
        ti.xcom_push('transformed_data', transformed_data)
        log(CarparkPublicPipeline, "Transform completed successfuly")

    def load(**kwargs):
        log(CarparkPublicPipeline, "Load Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='transform', key='transformed_data')
        CarparkPublicPipeline.load(data)
        log(CarparkPublicPipeline, "Load completed successfuly")

    extract = PythonOperator(task_id="extract", python_callable=extract)
    transform = PythonOperator(task_id="transform", python_callable=transform)
    load = PythonOperator(task_id="load", python_callable=load)
    extract >> transform >> load



    