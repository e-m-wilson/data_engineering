from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests

@dag
def user_processing():
    
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


    # ti is a reserved keyword in airflow for 'task instance'
    @task
    def extract_user(fake_user):
        return {
            "id": fake_user["id"],
            "firstName": fake_user["personalInfo"]["firstName"],
            "lastName": fake_user["personalInfo"]["lastName"],
            "email": fake_user["personalInfo"]["email"]
        }

    @task
    def process_user(user_info):
        import csv
        from datetime import datetime

        user_info["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("/tmp/user_info.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=user_info.keys())
            writer.writeheader()
            writer.writerow(user_info)

    @task
    def store_user():
        hook = PostgresHook(postgres_conn_id="postgres")
        hook.copy_expert(
            sql="COPY users FROM STDIN WITH CSV HEADER",
            filename="/tmp/user_info.csv"
        )

    # fake_user = is_api_available()
    # user_info = extract_user(fake_user)
    # process_user(user_info)
    # store_user()

    # define dependencies properly:
    # task_a >> task_b >> task_c
    # task_a >> [task_b, task_c] >> task_d
    # these can be on multiple lines as well
    # we can define like this since each functions expects a return value from the previous:
    process_user(extract_user(create_table >> is_api_available())) >> store_user()

user_processing()