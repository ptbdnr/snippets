import copy
import json
import logging
import pathlib
import uuid
from pathlib import Path

from datasets import DatasetDict, load_dataset

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

# ref. https://github.com/LC-John/Yahoo-Answers-Topic-Classification-Dataset/tree/master
HF_DATASETS_NAME = "community-datasets/yahoo_answers_topics"
CLASSES = [
    "Society & Culture",
    "Science & Mathematics",
    "Health",
    "Education & Reference",
    "Computers & Internet",
    "Sports",
    "Business & Finance",
    "Entertainment & Music",
    "Family & Relationships",
    "Politics & Government",
]


CORRELATION_ID = uuid.uuid4().hex[:4].upper()
OUTPUT_DIR = f"./../data/{CORRELATION_ID}-{HF_DATASETS_NAME.split('/')[-1]}"

pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

logger.info("HF datasets name: %s", HF_DATASETS_NAME)
logger.info("Output directory: %s", OUTPUT_DIR)
logger.info("Correlation ID: %s", CORRELATION_ID)

# HF datasets name: community-datasets/yahoo_answers_topics
# Output directory: ./../data/C6DF-yahoo_answers_topics
# Correlation ID: ABCD

# download datasets: train, validation, test


datasets = load_dataset(HF_DATASETS_NAME)  # doctest: +IGNORE_RESULT

logger.info("datasets: %s", list(datasets.keys()))
# datasets: ['train']


# Split the dataset into train, validation, and test sets
train = datasets["train"]
test_validtest = datasets["test"].train_test_split(test_size=0.5)

# Combine the splits into a DatasetDict
split_datasets = DatasetDict({
    "train": train,
    "validation": test_validtest["train"],
    "test": test_validtest["test"],
})

logger.info(split_datasets)

# DatasetDict({
#     train: Dataset({
#         features: ['id', 'topic', 'question_title', 'question_content', 'best_answer'],
#         num_rows: 1400000
#     })
#     validation: Dataset({
#         features: ['id', 'topic', 'question_title', 'question_content', 'best_answer'],
#         num_rows: 30000
#     })
#     test: Dataset({
#         features: ['id', 'topic', 'question_title', 'question_content', 'best_answer'],
#         num_rows: 30000
#     })
# })

# Rename columns in each split of the dataset

qa_template = {"prompt": "{prompt}", "completion": "{completion}"}
max_records = 2000

qa_dataset = {}
for split in split_datasets:
    logger.info("Processing split: %s", split)
    records = []
    for i in range(min(len(split_datasets[split]), max_records)):
        # print(f"Processing record: {i}")
        compiled_qa = copy.deepcopy(qa_template)
        prompt = " ".join([
            split_datasets[split][i]["question_title"],
            split_datasets[split][i]["question_content"],
            split_datasets[split][i]["best_answer"],
        ])
        compiled_qa["prompt"] = prompt
        compiled_qa["completion"] = CLASSES[split_datasets[split][i]["topic"]]
        records.append(compiled_qa)
    qa_dataset[split] = records

logger.info("=" * 16, "\n", "qa_dataset:")
logger.info(json.dumps(qa_dataset["train"][:2],indent=2))

# #Processing split: train
# Processing split: validation
# Processing split: test
# ================
#  qa_dataset:
# {
#   "train": [
#     {
#       "prompt": "why doesn't an optical mouse work on a glass table? or even on some surfaces? Optical mice use an LED and a camera to rapidly capture images of the surface beneath the mouse.  The infomation from the camera is analyzed by a DSP (Digital Signal Processor) and used to detect imperfections in the underlying surface and determine motion. Some materials, such as glass, mirrors or other very shiny, uniform surfaces interfere with the ability of the DSP to accurately analyze the surface beneath the mouse.  \\nSince glass is transparent and very uniform, the mouse is unable to pick up enough imperfections in the underlying surface to determine motion.  Mirrored surfaces are also a problem, since they constantly reflect back the same image, causing the DSP not to recognize motion properly. When the system is unable to see surface changes associated with movement, the mouse will not work properly.",
#       "completion": "Computers & Internet"
#     },


# Define the output file paths
output_files = {
    "train": f"{OUTPUT_DIR}/{CORRELATION_ID}-train.jsonl",
    "validation": f"{OUTPUT_DIR}/{CORRELATION_ID}-validation.jsonl",
    "test": f"{OUTPUT_DIR}/{CORRELATION_ID}-test.jsonl",
}

# Write each split to its respective file in JSONL format
for split, records in qa_dataset.items():
    with Path.open(output_files[split], "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

logger.info("Data exported to %s in JSONL format.", OUTPUT_DIR)

# Data exported to ./../data/ABCD-yahoo_answers_topics in JSONL format.
