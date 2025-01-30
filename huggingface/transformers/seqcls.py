# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Sequence classification task

# %%
# %pip install -r requirements.txt

# %%
# input constants
import os

import dotenv
import torch

dotenv.load_dotenv()

HF_DATASETS_NAME = "google-research-datasets/go_emotions"
HF_PRETRAINED_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # when debugging use "cpu" for better error messages 

EPOCHS = 1
BATCH_SIZE = 8
LEARNING_RATE = 0.1

OUTPUT_DIR = os.path.join("trained", HF_PRETRAINED_MODEL_NAME)

if DEVICE == "cuda":
    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

# %%
print(f"HF datasets name: {HF_DATASETS_NAME}")
print(f"HF pretrained model name: {HF_PRETRAINED_MODEL_NAME}")

print(f"Using {DEVICE} device")

print("=" * 5, "TRAINING", "=" * 5)
print(f"epochs: {EPOCHS}")
print(f"batch_size: {BATCH_SIZE}")
print(f"learning rate (lr): {LEARNING_RATE}")

# %% [markdown]
# # Data Downloading and Loading

# %%
# download datasets: train, validation, test
from datasets import load_dataset

datasets = load_dataset(HF_DATASETS_NAME)  # doctest: +IGNORE_RESULT

# %%
import json

print(f"datasets: {list(datasets)}")
label_ids = []
for dataset_key in datasets:
    print(f"len({dataset_key}): {len(datasets[dataset_key])}")
    [label_ids.append(label) for ls in datasets[dataset_key]["labels"] for label in ls]
label_ids = list(set(label_ids))
label_names = datasets["train"].features["labels"].feature.names
assert len(label_ids) == len(label_names)
label_ids.sort()
print(f"train dataset: {datasets["train"]}")
print(f"train dataset features: {datasets["train"].features}")
print(f"labelIds {len(label_ids)} unique, min {min(label_ids)}, max {max(label_ids)}, first 10: {label_ids[:10]}")
print(f"labelNames ({len(label_names)} unique), first 10: {label_names[:10]}")
for i in range(3):
    print(f"Example ({i}): {json.dumps(datasets["train"][i], indent=2)}")

# %%
# validate data
for key, dataset in datasets.items():
    for idx, record in enumerate(dataset):
        assert len(record["text"]) > 0, f"{key}:{idx} - Expected text, received '{record["text"]}'"
        assert len(record["labels"]) > 0, f"{key}:{idx} - Expected labels, received '{record["labels"]}'"
        for label in record["labels"]:
            assert isinstance(label, int), f"{key}:{idx} - Expected int label, received '{label}'"
            assert 0 <= label < len(label_ids), f"{key}:{idx} - Expected 0<=label<len(labelIds), received '{label}'"
print("Done")

# %% [markdown]
# # Model and Tokenizer

# %%
# using pipelines
from transformers import pipeline

sentiment_task = pipeline("sentiment-analysis", model=HF_PRETRAINED_MODEL_NAME, device=DEVICE)
sentiment_task("Covid cases are increasing fast!")

# %%
# download tokenizer, config, model
# use_fast: False for Python-based algo when encoding is non-trivial (default), True for Rust-base algo with trivial encoding
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(HF_PRETRAINED_MODEL_NAME, use_fast=False, device=DEVICE)
base_config = AutoConfig.from_pretrained(HF_PRETRAINED_MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(
    pretrained_model_name_or_path=HF_PRETRAINED_MODEL_NAME
)
model.to(device=DEVICE)

# %%
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=DEVICE)
classifier(inputs="This is super cool!")

# %%
# test inference
from scipy.special import softmax
from torch import nn
from transformers import AutoConfig

input_text = datasets["train"][0]["text"]
print(f"==INPUT TEXT==:\n{input_text}")
expected_labels = datasets["train"][0]["labels"]
print(f"==EXPECTED==:\n{[f'{label_names[label]} ({label})' for label in expected_labels]}")
encoded_inputs = tokenizer(input_text, return_tensors="pt").to(device=DEVICE)
outputs = model(**encoded_inputs)
logits = outputs[0][0].detach()
scores = softmax(logits.to("cpu"))
config = AutoConfig.from_pretrained(HF_PRETRAINED_MODEL_NAME)
print(f"==OUTPUT==:\n{[{config.id2label[i]: scores[i]} for i in range(len(logits))]}")


# %% [markdown]
# # Finetuning configuration

# %%
# download model with target number of labels
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    pretrained_model_name_or_path=HF_PRETRAINED_MODEL_NAME,
    num_labels=max(label_ids),
    ignore_mismatched_sizes=True  # because original model's num_labels < expected model's num_labels 
)
model.to(device=DEVICE)

# %%
print(f"Number of (optionally, trainable or non-embeddings) parameters: {model.num_parameters():,}")


# %%
# tokenize the dataset
# Hugging Face Transformers models expect tokenized input, rather than a string text.
def tokenize_dataset(dataset):
    # encode text to input_ids and attention_mask
    encoded_text = tokenizer(
        text=dataset["text"],
        padding="max_length",  # add special padding token to create uniform-length inputs of "max_length"
        truncation=True,  # truncate to "max_length"
        max_length=base_config.max_position_embeddings,
        return_tensors="pt")
    dataset["input_ids"] = encoded_text.input_ids
    dataset["attention_mask"] = encoded_text.attention_mask
    # encode labels from List[List[int]] to List[int]
    first_labels = []
    for labels in dataset["labels"]:
        first_label = labels[0]
        first_labels.append(first_label)
    # print(f"first labels {len(set(first_labels))} unique, min {min(first_labels)} max {max(first_labels)}")
    dataset["labels"] = first_labels
    return dataset

encoded_datasets = datasets.map(
    tokenize_dataset,
    batched=True,
    remove_columns=["id", "text"],
)

# %%
import json

print(f"datasets: {list(encoded_datasets)}")
for dataset_key in encoded_datasets:
    print(f"len({dataset_key}): {len(encoded_datasets[dataset_key])}")
print(f"train dataset: {encoded_datasets["train"]}")
print(f"train dataset features: {encoded_datasets["train"].features}")
for i in range(3):
    print(f"Example ({i}): {json.dumps(encoded_datasets["train"][i])}")

# %% [markdown]
# # Training Job

# %%
# data loader/collator to batch input in training and evaluation datasets
# DataCollatorWithPadding pads dynamically your text to the length of the longest element in its batch, 
# so they are a uniform length
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# %%
# configure evaluation metrics in addition to the default `loss` metric that the `Trainer` computes
import evaluate
import numpy as np

metric = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


# %%
# clean up the GPU memory
if DEVICE == "gpu":
    from numba import cuda
    device = cuda.get_current_device()
    device.reset()

# %%
# [OPTIONAL] TROUBLESHOOTING
# huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
# To disable this warning, you can either:
#	- Avoid using `tokenizers` before the fork if possible
#	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
# See: https://github.com/huggingface/transformers/issues/5486
os.environ["TOKENIZERS_PARALLELISM"] = "true"  # default: "false"

# %%
# train job config
# Hugging Face training configuration tools can be used to configure a <T>Trainer.
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    #do_train=True,
    #do_eval=True,

    num_train_epochs=1,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=LEARNING_RATE,

    weight_decay=0.01,
    #gradient_accumulation_steps=2,  # default 1
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    # metric_for_best_model="f1"

    fp16=True,  # lower precision
    # use_ipex=True if DEVICE == "cpu" else False,  # use Intel extension for PyTorch
    use_cpu=DEVICE == "cpu"  # False will use CUDA or MPS if available
)

# %%
# [OPTIONAL] TROUBLESHOOTHING
# IF
# RuntimeError: CUDA error: device-side assert triggered
# CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
# For debugging consider passing CUDA_LAUNCH_BLOCKING=1
# Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["TORCH_USE_CUDA_DSA"] = "1"
# IF still errors out try DEVICE = "cpu" to see error message

# %%
# The <T>Trainer classes require the user to provide: 1) Metrics 2) A base model 3) A training configuration
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_datasets["train"],
    eval_dataset=encoded_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    # compute_metrics=compute_metrics
)

# %%
# if using GPU, then during training job monitor compute instance in terminal with cli command `nvidia-smi`
trainer.train()

# %% [markdown]
# # Store model

# %%
model.save_pretrained(OUTPUT_DIR)
