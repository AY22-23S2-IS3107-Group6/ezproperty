from datetime import datetime
from db.etl import get_all_pipelines
from db.etl.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator

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
        pipeline.schema_name, # needs to be string which class name isn't, will add variables to indiv etls
        default_args=pipeline.default_args,
        description=pipeline.description,
        schedule_interval=pipeline.schedule_interval,
        start_date=datetime(2021, 1, 1), # can consider adding to indiv etls
        catchup=False, # can consider adding to indiv etls
        tags=pipeline.tags,
    )

    with dag:
        dag.doc_md = __doc__
        extract = PythonOperator(task_id="extract", python_callable=extract)
        transform = PythonOperator(task_id="transform", python_callable=transform)
        load = PythonOperator(task_id="load", python_callable=load)
        extract >> transform >> load

    return dag


def write_dag_to_file(dag):

    dag_file = 'airflow/dags/{}.py'.format(dag.dag_id)

    with open(dag_file, 'w') as f:
        print(dag)
        # f.write(dag) need to get this dag source code and write it into dags folder I think

    print(f"DAG {dag.dag_id} has been written to {dag_file}")

for pipeline in get_all_pipelines(False):
    globals()[pipeline.id] = create_dag(pipeline=pipeline)
    write_dag_to_file(globals()[pipeline.id])


    