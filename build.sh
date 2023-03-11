#!/bin/bash

[ ! -d "./env" ] && echo "*** Creating Virtual Environment ***"
[ ! -d "./env" ] && virtualenv env
source env/bin/activate

export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
export AIRFLOW_VERSION="2.2.3"

echo "*** Downloading Libraries ***"
[ ! -d "./env/lib/python3.8/site-packages/airflow" ] && pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
[ ! -d "./env/lib/python3.8/site-packages/mysql" ] && pip install mysql-connector-python
[ ! -d "./env/lib/python3.8/site-packages/pymongo" ] && pip install pymongo
echo "*** Libraries Downloaded ***"

echo "*** Initialising Airflow DB ***"
airflow db init
airflow users create -u admin -f John -l Doe --role Admin -p password
