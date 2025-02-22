"""DAG with Operators.

This DAG demonstrates the use of PythonOperator to create a simple data pipeline.
In this case, the pipeline has three tasks: extract, transform, and load.
Compared to the TaskFlow API example, this example uses PythonOperators to create the DAG.
"""

import json
import logging
import textwrap

import pendulum

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

with DAG(
    "tutorial_dag",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    description="DAG tutorial",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    dag.doc_md = __doc__

    def extract(**kwargs) -> None:
        """Extract task to get data ready for the rest of the data pipeline."""
        ti = kwargs["ti"]
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        ti.xcom_push("order_data", data_string)

    def transform(**kwargs) -> None:
        """Transform task to compute the total order value."""
        ti = kwargs["ti"]
        extract_data_string = ti.xcom_pull(task_ids="extract", key="order_data")
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push("total_order_value", total_value_json_string)

    def load(**kwargs) -> None:
        """Load task to print the total order value."""
        ti = kwargs["ti"]
        total_value_string = ti.xcom_pull(task_ids="transform", key="total_order_value")
        total_order_value = json.loads(total_value_string)
        logging.info(total_order_value)

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract,
    )
    extract_task.doc_md = textwrap.dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform,
    )
    transform_task.doc_md = textwrap.dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load,
    )
    load_task.doc_md = textwrap.dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """,
    )

    extract_task >> transform_task >> load_task
