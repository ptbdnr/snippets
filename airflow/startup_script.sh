# Set Airflow Home (optional)

export AIRFLOW_HOME=~/workspace/snippets/airflow


# Install Airflow using the constraints file, which is determined based on the URL we pass:

AIRFLOW_VERSION=2.10.4

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.10.4 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"


# Run Airflow Standalone

airflow standalone


# Access the Airflow UI
# Visit http://localhost:8080 in your browser 
# and log in with the admin account details shown in the terminal. 


# Command Line Metadata Validation
# initialize the database tables
airflow db migrate
# print the list of active DAGs
airflow dags list
# prints the list of tasks in the "tutorial" DAG
airflow tasks list tutorial
# prints the hierarchy of tasks in the "tutorial" DAG
airflow tasks list tutorial --tree
