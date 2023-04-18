import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
from db.etl.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from db.etl.hawkerCentre import HawkerCentrePipeline

def log(pipeline: Pipeline, message: str):
    print(f"Airflow  | {pipeline.schema_name.ljust(26)} | {message}")

default_args = {
    'owner': 'airflow',
}

with DAG(
    'hawkerCentre',
    default_args=default_args,
    description='Loads Hawker Centres',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['is3107g6','amn'],
) as dag:

    dag.doc_md = __doc__
    HawkerCentrePipelineTemp = HawkerCentrePipeline()

    def extract(**kwargs):
        log(HawkerCentrePipeline, "Extract start")
        ti = kwargs['ti']
        data = HawkerCentrePipelineTemp.extract()
        ti.xcom_push('data', data)
        log(HawkerCentrePipelineTemp, "Extract completed successfuly")

    def transform(**kwargs):
        log(HawkerCentrePipelineTemp, "Transform Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='extract', key='data')
        transformed_data = HawkerCentrePipelineTemp.transform(data)
        ti.xcom_push('transformed_data', transformed_data)
        log(HawkerCentrePipelineTemp, "Transform completed successfuly")

    def load(**kwargs):
        log(HawkerCentrePipelineTemp, "Load Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='transform', key='transformed_data')
        HawkerCentrePipelineTemp.load(data)
        log(HawkerCentrePipelineTemp, "Load completed successfuly")

    extract = PythonOperator(task_id="extract", python_callable=extract)
    transform = PythonOperator(task_id="transform", python_callable=transform)
    load = PythonOperator(task_id="load", python_callable=load)
    extract >> transform >> load