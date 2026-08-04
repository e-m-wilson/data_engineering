from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
import requests
from airflow.providers.standard.operators.python import PythonOperator

# ti is a reserved keyword in airflow for 'task instance'
def _extract_user(ti):
    fake_user = ti.xcom_pull(task_ids="is_api_available")
    
    # to test this we can comment out the above line for xcom, and uncomment the following two lines:
    # airflow tasks test user_processing extract_user
    # response = requests.get("https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json")
    # fake_user = response.json()
    
    
    print(fake_user)
    return {
        "id": fake_user["id"],
        "firstName": fake_user["personalInfo"]["firstName"],
        "lastName": fake_user["personalInfo"]["lastName"],
        "email": fake_user["personalInfo"]["email"]
    }


@dag
def user_processing_old():
    
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres",
        sql="""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            firstName VARCHAR(255),
            lastName VARCHAR(255),
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    
    # check if endpoint is available every 30 seconds
    # if not available after 300 seconds, timeout the operation 
    @task.sensor(poke_interval=30, timeout=300)
    def is_api_available() -> PokeReturnValue:
        response = requests.get("https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json")
        print(response.status_code)
        if response.status_code == 200:
            condition = True
            fake_user = response.json()
        else:
            condition = False
            fake_user = None
        return PokeReturnValue(is_done=condition, xcom_value=fake_user)

    extract_user = PythonOperator(
        task_id="extract_user",
        python_callable=_extract_user
    )

    is_api_available()

user_processing_old()