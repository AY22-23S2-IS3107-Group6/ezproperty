import json
import requests
from datetime import datetime
from textwrap import dedent
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
}


with DAG(
    'dataInit',
    default_args=default_args,
    description='Data Initialisation for IS3107 Project',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    dag.doc_md = __doc__
    def get_block_num(**kwargs):
        ti = kwargs['ti']
        x = requests.get('https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=WSEJ4BEAXN5TIFIKQBIXC7UB7MEA5VZFZI')
        x_dict = x.json()
        print("block number: " + x_dict.get("result"))
        ti.xcom_push('latestBlock', x_dict.get("result"))
    def get_transaction_num(**kwargs):
        ti = kwargs['ti']
        extract_data_string = ti.xcom_pull(task_ids='get_block_num', key='latestBlock')
        x = requests.get(f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={extract_data_string}&boolean=true&apikey=WSEJ4BEAXN5TIFIKQBIXC7UB7MEA5VZFZI')
        x_dict = x.json()
        result = x_dict.get("result")
        transactions = result.get("transactions")
        print("txs number: " + str(len(transactions)))


    get_block_num_task = PythonOperator(task_id='get_block_num', python_callable=get_block_num,)
    get_transaction_num_task = PythonOperator(task_id='get_transaction_num', python_callable=get_transaction_num,)

    get_block_num_task >> get_transaction_num_task
