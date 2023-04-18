import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
from db.etl.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from db.etl.rentalPropertyMedian import RentalPropertyMedianPipeline

def log(pipeline: Pipeline, message: str):
    print(f"Airflow  | {pipeline.schema_name.ljust(26)} | {message}")

default_args = {
    'owner': 'airflow',
}

with DAG(
    'rentalPropertyMedian',
    default_args=default_args,
    description='Loads Rental Property Median',
    schedule_interval='@monthly',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['is3107g6','main'],
) as dag:

    dag.doc_md = __doc__
    RentalPropertyMedianPipelineTemp = RentalPropertyMedianPipeline()

    def extract(**kwargs):
        log(RentalPropertyMedianPipeline, "Extract start")
        ti = kwargs['ti']
        data = RentalPropertyMedianPipelineTemp.extract()
        ti.xcom_push('data', data)
        log(RentalPropertyMedianPipelineTemp, "Extract completed successfuly")

    def transform(**kwargs):
        log(RentalPropertyMedianPipelineTemp, "Transform Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='extract', key='data')
        transformed_data = RentalPropertyMedianPipelineTemp.transform(data)
        ti.xcom_push('transformed_data', transformed_data)
        log(RentalPropertyMedianPipelineTemp, "Transform completed successfuly")

    def load(**kwargs):
        log(RentalPropertyMedianPipelineTemp, "Load Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='transform', key='transformed_data')
        RentalPropertyMedianPipelineTemp.load(data)
        log(RentalPropertyMedianPipelineTemp, "Load completed successfuly")

    extract = PythonOperator(task_id="extract", python_callable=extract)
    transform = PythonOperator(task_id="transform", python_callable=transform)
    load = PythonOperator(task_id="load", python_callable=load)
    extract >> transform >> load