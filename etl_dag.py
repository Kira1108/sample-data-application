import sys
import os
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))
from airflow import DAG
from operators.wecom_operator import failure_callback_wecom
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from ingest import app


args={ 'on_failure_callback': failure_callback_wecom,
    'owner': 'wanghuan',
    'email': ['wanghuan@tidis.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
}


with DAG(
    dag_id='oil_prices',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(1), 
    tags=['wti','brent'],
) as dag:

    task1 = PythonOperator(
        task_id = 'oil_price_extractor',
        python_callable = app,
        dag = dag,)