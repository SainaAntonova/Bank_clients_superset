from airflow import DAG

from airflow.operators.bash_operator import BashOperator

import os
from datetime import datetime
import time


default_args = {
    'owner': 'Igor',
    'start_date': datetime(2024, 1, 1),
}

with DAG(dag_id='bank_database_update3', default_args=default_args, schedule_interval=None) as dag:

    download_user_data_task = BashOperator(
        task_id='download_user_data',
        bash_command='docker exec -i postgres_1 wget -O /var/lib/postgresql/new_clients.csv https://9c579ca6-fee2-41d7-9396-601da1103a3b.selstorage.ru/new_clients.csv'
    )

    load_to_postgres_task = BashOperator(
        task_id='load_to_postgres',
        bash_command='docker exec -i postgres_1 psql -U postgres -d creditdb -c \
                    "\\copy credit_clients(Date, CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited) FROM \'/var/lib/postgresql/new_clients.csv\' DELIMITER \';\' CSV HEADER"',
    )
    

    download_user_data_task >> load_to_postgres_task
