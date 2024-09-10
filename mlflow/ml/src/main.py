import subprocess

import mlflow

# if using Azure Machine Learning Studio
# from azureml.core import Workspace
# azure_ml_tracking_uri = Workspace.from_config().get_mlflow_tracking_uri()
# mlflow.set_tracking_uri(azure_ml_tracking_uri)

mlflow.set_experiment(experiment_name="an_experiment")

current_git_revision_hash = (
    subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
)

mlflow.set_experiment_tags(
    tags={
        "exp_tag": "an_experiment_tag",
        "git_revision_hash": current_git_revision_hash,
    }
)

with mlflow.start_run(run_name="a_run") as run:
    # tags
    mlflow.set_tags({"run_tag": "a_run_tag"})

    # log input
    mlflow.log_text("input content", "input.txt")
    mlflow.log_param("param_1", 0)
    mlflow.log_params({"param_2": 1, "param_3": 2})

    # log output
    mlflow.log_metric("metric_1", 1)
    mlflow.log_metrics({"metric_2": 2, "metric_3": 3})
