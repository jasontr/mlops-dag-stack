from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'datascience',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['datascience@example.com']
}

dag = DAG(
    'sum',
    schedule_interval='*/5 * * * *',
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
    default_args=default_args,
    description='DAG that sums the total of generated count values.'
)

t1 = PostgresOperator(
    task_id='if_not_exists',
    postgres_conn_id='openlineage-example',
    sql='''
    CREATE TABLE IF NOT EXISTS sums (
      value INTEGER
    );''',
    dag=dag
)

t2 = PostgresOperator(
    task_id='total',
    postgres_conn_id='openlineage-example',
    sql='''
    INSERT INTO sums (value)
        SELECT SUM(c.value) FROM counts AS c;
    ''',
    dag=dag
)

t1 >> t2