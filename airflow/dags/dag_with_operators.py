"""Defines an Airflow DAG with tasks.

Demonstrates the use of BashOperator and PythonOperator, as well as task dependencies.
"""

import logging
import textwrap
from datetime import datetime, timezone

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# A DAG represents a workflow, a collection of tasks
with DAG(
    dag_id="demo_dag_with_operators",
    start_date=datetime(2022, 1, 1, tzinfo=timezone.utc),
    schedule="0 0 * * *",
    tags=["demo"],
) as dag:
    # Tasks are represented as operators
    bash_command = BashOperator(
        task_id="bash_command",
        bash_command="echo hello",
        depends_on_past=False,
        retries=2,
    )
    bash_command.doc_md = textwrap.dedent("""\
    #### Task Documentation
    You can document your task using the attributes
    `doc_md` (markdown),
    `doc` (plain text),
    `doc_rst`, `doc_json`, `doc_yaml`
    which gets rendered in the UI's Task Instance Details page.
    ![img](https://imgs.xkcd.com/comics/fixing_problems.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """)

    python_function = PythonOperator(
        task_id="python_function",
        python_callable=lambda: logger.info("Hello from Python!"),
    )

    @task()
    def airflow() -> None:
        """Log an informational message about Airflow."""
        logger.info("airflow")

    templated_command = textwrap.dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """,
    )

    templated = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    # Set dependencies between tasks
    bash_command >> [python_function, airflow()] >> templated
