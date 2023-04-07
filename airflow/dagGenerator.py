from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from ..db.etl.pipeline import Pipeline
from ..db.etl import get_all_pipelines


def log(pipeline: Pipeline, message: str):
    print(f"Airflow  | {pipeline.schema_name.ljust(26)} | {message}")


def create_dag(pipeline: Pipeline) -> DAG:

    def extract(**kwargs):
        log(pipeline, "Extract start")
        ti = kwargs['ti']
        data = pipeline.extract()
        ti.xcom_push('data', data)
        log(pipeline, "Extract completed successfuly")

    def transform(**kwargs):
        log(pipeline, "Transform Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='extract', key='data')
        transformed_data = pipeline.transform(data)
        ti.xcom_push('transformed_data', transformed_data)
        log(pipeline, "Transform completed successfuly")

    def load(**kwargs):
        log(pipeline, "Load Start")
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='transform', key='transformed_data')
        pipeline.load(data)
        log(pipeline, "Load completed successfuly")

    dag = DAG(
        pipeline.id,
        default_args=pipeline.default_args,
        description=pipeline.description,
        schedule_interval=pipeline.schedule_interval,
        start_date=pipeline.start_date,
        catchup=pipeline.catchup,
        tags=pipeline.tags,
    )

    with dag:
        dag.doc_md = __doc__
        extract = PythonOperator(task_id="extract", python_callable=extract)
        transform = PythonOperator(task_id="transform",
                                   python_callable=transform)
        load = PythonOperator(task_id="load", python_callable=load)
        extract >> transform >> load

    return dag


for pipeline in get_all_pipelines(False):
    globals()[pipeline.id] = create_dag(pipeline=pipeline)