import dotenv
import mlflow
import pandas as pd

dotenv.load_dotenv()

eval_data = pd.DataFrame(
    {
        "inputs": [
            "What is MLflow?",
            "What is Spark?",
        ],
        "ground_truth": [
            "MLflow is an open-source platform for managing the end-to-end machine learning (ML) lifecycle. "
            "It was developed by Databricks, a company that specializes in big data and machine learning solutions. "
            "MLflow is designed to address the challenges that data scientists and machine learning engineers "
            "face when developing, training, and deploying machine learning models.",
            "Apache Spark is an open-source, distributed computing system designed for big data processing and "
            "analytics. It was developed in response to limitations of the Hadoop MapReduce computing model, "
            "offering improvements in speed and ease of use. Spark provides libraries for various tasks such as "
            "data ingestion, processing, and analysis through its components like Spark SQL for structured data, "
            "Spark Streaming for real-time data processing, and MLlib for machine learning tasks",
        ],
        "predictions": [
            "MLflow is an open-source platform that provides handy tools to manage Machine Learning workflow "
            "lifecycle in a simple way",
            "Spark is a popular open-source distributed computing system designed for big data processing and analytics.",
        ],
    }
)

with mlflow.start_run() as run:
    results = mlflow.evaluate(
        data=eval_data,
        targets="ground_truth",
        predictions="predictions",
        extra_metrics=[mlflow.metrics.genai.answer_similarity()],
        evaluators="default",
    )
    print(f"See aggregated evaluation results below: \n{results.metrics}")

    eval_table = results.tables["eval_results_table"]
    print(f"See evaluation table below: \n{eval_table}")
