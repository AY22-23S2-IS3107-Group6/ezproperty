import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
from db.etl.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from db.etl.primarySchool import PrimarySchoolPipeline

def log(pipeline: Pipeline, message: str):
    print(f"Airflow  | {pipeline.schema_name.ljust(26)} | {message}")

default_args = {
    'owner': 'airflow',
}

with DAG(
    'primarySchool',
    default_args=default_args,
    description='Loads Primary Schools',
    schedule_interval='@monthly',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['is3107g6','amn'],
) as dag:

    dag.doc_md = __doc__
    PrimarySchoolPipelineTemp = PrimarySchoolPipeline(run_pipeline=False)

    def extract(**kwargs):
        log(PrimarySchoolPipeline, "Extract start")
        ti = kwargs['ti']
        data = PrimarySchoolPipelineTemp.extract()
        ti.xcom_push('data', json.dumps(data, default=str))
        log(PrimarySchoolPipelineTemp, "Extract completed successfuly")

    def transform(**kwargs):
        log(PrimarySchoolPipelineTemp, "Transform Start")
        ti = kwargs['ti']
        data = json.loads(ti.xcom_pull(task_ids='extract', key='data'))
        transformed_data = PrimarySchoolPipelineTemp.transform(data)
        ti.xcom_push('transformed_data', json.dumps(transformed_data, default=str))
        log(PrimarySchoolPipelineTemp, "Transform completed successfuly")

    def load(**kwargs):
        log(PrimarySchoolPipelineTemp, "Load Start")
        ti = kwargs['ti']
        data = json.loads(ti.xcom_pull(task_ids='transform', key='transformed_data'))
        PrimarySchoolPipelineTemp.load(data)
        log(PrimarySchoolPipelineTemp, "Load completed successfuly")

    extract = PythonOperator(task_id="extract", python_callable=extract)
    transform = PythonOperator(task_id="transform", python_callable=transform)
    load = PythonOperator(task_id="load", python_callable=load)
    extract >> transform >> load