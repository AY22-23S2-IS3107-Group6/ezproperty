import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
from db.etl.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from db.etl.propertyInfo import PropertyInformationPipeline

def log(pipeline: Pipeline, message: str):
    print(f"Airflow  | {pipeline.schema_name.ljust(26)} | {message}")

default_args = {
    'owner': 'airflow',
}

with DAG(
    'propertyInfo',
    default_args=default_args,
    description='Loads Property Info',
    schedule_interval='@monthly',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['is3107g6','ref'],
) as dag:

    dag.doc_md = __doc__
    PropertyInformationPipelineTemp = PropertyInformationPipeline(run_pipeline=False)

    def extract(**kwargs):
        log(PropertyInformationPipeline, "Extract start")
        ti = kwargs['ti']
        data = PropertyInformationPipelineTemp.extract()
        ti.xcom_push('data', json.dumps(data, default=str))
        log(PropertyInformationPipelineTemp, "Extract completed successfuly")

    def transform(**kwargs):
        log(PropertyInformationPipelineTemp, "Transform Start")
        ti = kwargs['ti']
        data = json.loads(ti.xcom_pull(task_ids='extract', key='data'))
        transformed_data = PropertyInformationPipelineTemp.transform(data)
        ti.xcom_push('transformed_data', json.dumps(transformed_data, default=str))
        log(PropertyInformationPipelineTemp, "Transform completed successfuly")

    def load(**kwargs):
        log(PropertyInformationPipelineTemp, "Load Start")
        ti = kwargs['ti']
        data = json.loads(ti.xcom_pull(task_ids='transform', key='transformed_data'))
        PropertyInformationPipelineTemp.load(data)
        log(PropertyInformationPipelineTemp, "Load completed successfuly")

    extract = PythonOperator(task_id="extract", python_callable=extract)
    transform = PythonOperator(task_id="transform", python_callable=transform)
    load = PythonOperator(task_id="load", python_callable=load)
    extract >> transform >> load