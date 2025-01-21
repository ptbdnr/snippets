import copy
import json
import logging
import uuid
from collections import defaultdict
from pathlib import Path

import numpy as np
import tiktoken  # for token counting
from datasets import DatasetDict, load_dataset

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

HF_DATASETS_NAME = "harpreetsahota/modern-to-shakesperean-translation"


CORRELATION_ID = uuid.uuid4().hex[:4].upper()
OUTPUT_DIR = f"./../data/{CORRELATION_ID}-{HF_DATASETS_NAME.split('/')[-1]}"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

logger.info("HF datasets name: %s", HF_DATASETS_NAME)
logger.info("Output directory: %s", OUTPUT_DIR)
logger.info("Correlation ID: %s", CORRELATION_ID)

# HF datasets name: harpreetsahota/modern-to-shakesperean-translation
# Output directory: ./../data/4314-modern-to-shakesperean-translation
# Correlation ID: ABCD

# download datasets: train, validation, test

datasets = load_dataset(HF_DATASETS_NAME)  # doctest: +IGNORE_RESULT

logger.info("datasets: %s", list(datasets))

# datasets: ['train']


# Split the dataset into train, validation, and test sets
train_testvalid = datasets["train"].train_test_split(test_size=0.2)
test_valid = train_testvalid["test"].train_test_split(test_size=0.5)

# Combine the splits into a DatasetDict
split_datasets = DatasetDict({
    "train": train_testvalid["train"],
    "validation": test_valid["train"],
    "test": test_valid["test"],
})

logger.info(split_datasets)

# DatasetDict({
#     train: Dataset({
#         features: ['modern', 'shakespearean'],
#         num_rows: 219
#     })
#     validation: Dataset({
#         features: ['modern', 'shakespearean'],
#         num_rows: 27
#     })
#     test: Dataset({
#         features: ['modern', 'shakespearean'],
#         num_rows: 28
#     })
# })

# Rename columns in each split of the dataset

messages_template = {"messages": [
    {"role": "system", "content": "Translate this."},
    {"role": "user", "content": "{prompt}"},
    {"role": "assistant", "content": "{completion}"}],
}

chat_message_dataset = {}
for split in split_datasets:
    logger.info("Processing split: %s", split)
    records = []
    for i in range(len(split_datasets[split])):
        # print(f"Processing record: {i}")
        compiled_messages = copy.deepcopy(messages_template)
        compiled_messages["messages"][1]["content"] = split_datasets[split][i]["modern"]
        compiled_messages["messages"][2]["content"] = split_datasets[split][i]["shakespearean"]
        records.append(compiled_messages)
    chat_message_dataset[split] = records

logger.info("=" * 16, "\n", "chat_message_dataset:")
logger.info(json.dumps(chat_message_dataset,indent=2)[:500])

# Processing split: train
# Processing split: validation
# Processing split: test
# ================
#  chat_message_dataset:
# {
#   "train": [
#     {
#       "messages": [
#         {
#           "role": "system",
#           "content": "Translate this."
#         },
#         {
#           "role": "user",
#           "content": "That's dope"
#         },
#         {
#           "role": "assistant",
#           "content": "Verily, 'tis wondrous"
#         }
#       ]
#     },


# Define the output file paths
output_files = {
    "train": f"{OUTPUT_DIR}/{CORRELATION_ID}-train.jsonl",
    "validation": f"{OUTPUT_DIR}/{CORRELATION_ID}-validation.jsonl",
    "test": f"{OUTPUT_DIR}/{CORRELATION_ID}-test.jsonl",
}

# Write each split to its respective file in JSONL format
for split, records in chat_message_dataset.items():
    with Path(output_files[split], "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

logger.info("Data exported to %s in JSONL format.", OUTPUT_DIR)

# Data exported to ./../data/ABCD-modern-to-shakesperean-translation in JSONL format.

#| # Cost estimation
#| ref. https://cookbook.openai.com/examples/chat_finetuning_data_prep


# Initial dataset stats
dataset = chat_message_dataset["train"]
logger.info("Num examples: %s", len(dataset))
logger.info("First example:")
for message in dataset[0]["messages"]:
    logger.info(message)

# Num examples: 219
# First example:
# {'role': 'system', 'content': 'Translate this.'}
# {'role': 'user', 'content': "That's dope"}
# {'role': 'assistant', 'content': "Verily, 'tis wondrous"}

# Format error checks
format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue

    for message in messages:
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1

        if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
            format_errors["message_unrecognized_key"] += 1

        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1

        content = message.get("content", None)
        function_call = message.get("function_call", None)

        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1

    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

if format_errors:
    logger.info("Found errors:")
    for k, v in format_errors.items():
        logger.info("%s: %s", k, v)
else:
    logger.info("No errors found")

# No errors found

encoding = tiktoken.get_encoding("cl100k_base")

# not exact!
# simplified from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb


def num_tokens_from_messages(messages: list[dict], tokens_per_message: int =3, tokens_per_name: int=1) -> int:
    """Calculate the number of tokens from a list of messages.

    Args:
        messages (list): A list of message dictionaries.
        tokens_per_message (int): Number of tokens per message.
        tokens_per_name (int): Number of tokens per name.

    Returns:
        int: Total number of tokens.

    """
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

def num_assistant_tokens_from_messages(messages: list[dict]) -> int:
    """Calculate the number of tokens for assistant messages.

    Args:
        messages (List[Dict[str, str]]): A list of message dictionaries.

    Returns:
        int: Total number of tokens for assistant messages.

    """
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens

def print_distribution(values: list, name: str) -> None:
    """Print the distribution statistics of a list of values.

    Args:
        values (list): A list of numerical values.
        name (str): The name of the distribution being printed.

    Returns:
        None

    """
    logger.info("\n#### Distribution of %s:", name)
    logger.info("min / max: %s, %s", min(values), max(values))
    logger.info("mean / median: %s, %s", np.mean(values), np.median(values))
    logger.info("p5 / p95: %s, %s", np.quantile(values, 0.1), np.quantile(values, 0.9))


# Warnings and tokens counts
n_missing_system = 0
n_missing_user = 0
n_messages = []
convo_lens = []
assistant_message_lens = []

for ex in dataset:
    messages = ex["messages"]
    if not any(message["role"] == "system" for message in messages):
        n_missing_system += 1
    if not any(message["role"] == "user" for message in messages):
        n_missing_user += 1
    n_messages.append(len(messages))
    convo_lens.append(num_tokens_from_messages(messages))
    assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

logger.info("Num examples missing system message: %s", n_missing_system)
logger.info("Num examples missing user message: %s", n_missing_user)
print_distribution(n_messages, "num_messages_per_example")
print_distribution(convo_lens, "num_total_tokens_per_example")
print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
n_too_long = sum(l > 16385 for l in convo_lens)
logger.info("\n%s examples may be over the 16,385 token limit, they will be truncated during fine-tuning", n_too_long)

# Num examples missing system message: 0
# Num examples missing user message: 0

# #### Distribution of num_messages_per_example:
# min / max: 3, 3
# mean / median: 3.0, 3.0
# p5 / p95: 3.0, 3.0

# #### Distribution of num_total_tokens_per_example:
# min / max: 23, 119
# mean / median: 42.337899543378995, 42.0
# p5 / p95: 29.0, 53.0

# #### Distribution of num_assistant_tokens_per_example:
# min / max: 3, 51
# mean / median: 13.812785388127853, 13.0
# p5 / p95: 6.800000000000001, 20.200000000000017

# 0 examples may be over the 16,385 token limit, they will be truncated during fine-tuning

# Pricing and default n_epochs estimate
MAX_TOKENS_PER_EXAMPLE = 16385

TARGET_EPOCHS = 3
MIN_TARGET_EXAMPLES = 100
MAX_TARGET_EXAMPLES = 25000
MIN_DEFAULT_EPOCHS = 1
MAX_DEFAULT_EPOCHS = 25

n_epochs = TARGET_EPOCHS
n_train_examples = len(dataset)
if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
    n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
    n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

n_billing_tokens_in_dataset = sum(min(MAX_TOKENS_PER_EXAMPLE, length) for length in convo_lens)
logging.info("Dataset has ~%s tokens that will be charged for during training", n_billing_tokens_in_dataset)
logging.info("By default, you'll train for %s epochs on this dataset", n_epochs)
logging.info("By default, you'll be charged for ~%s tokens", n_epochs * n_billing_tokens_in_dataset)

# Dataset has ~9272 tokens that will be charged for during training
# By default, you'll train for 3 epochs on this dataset
# By default, you'll be charged for ~27816 tokens
