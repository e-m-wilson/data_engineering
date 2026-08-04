from airflow.sdk import asset, Asset, Context

@asset(
    schedule="@daily",
    uri="https://randomuser.me/api/"
)
def user(self) -> dict[str]:
    import requests

    r = requests.get(self.uri)
    return r.json()

# We refactor all this later to materialize both at once 
# @asset(
#     schedule=user
# )
# def user_location(user: Asset, context: Context) -> dict[str]:
#     user_data = context['ti'].xcom_pull(
#         dag_id=user.name,
#         task_ids=user.name,
#         include_prior_dates=True
#     )
#     return user_data['results'][0]['location']

# @asset(
#     schedule=user
# )
# def user_login(user: Asset, context: Context) -> dict[str]:
#     user_data = context['ti'].xcom_pull(
#         dag_id=user.name,
#         task_ids=user.name,
#         include_prior_dates=True
#     )
#     return user_data['results'][0]['login']

@asset.multi(
    schedule=user,
    outlets=[
        Asset(name="user_location"),
        Asset(name="user_login")
    ]
)
def user_info(user: Asset, context: Context) -> list[dict[str]]:
    user_data = context['li'].xcom_pull(
        dag_id=user.name,
        task_ids=user.name,
        include_prior_dates=True
    )
    return [
        user_data['results'][0]['location'],
        user_data['results'][0]['login']
    ]