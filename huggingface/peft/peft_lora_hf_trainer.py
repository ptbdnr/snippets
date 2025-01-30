# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernel_info:
#     name: python3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Parameter-Efficient Finetuning (PEFT) with Low-Level Adaptation (LORA) using HuggingFace PEFT on a single GPU

# %% jupyter={"outputs_hidden": false, "source_hidden": false} nteract={"transient": {"deleting": false}}
# %pip install -q -r requirements.txt

# %% gather={"logged": 1721941151683}
# input constants
import os

import dotenv

dotenv.load_dotenv()

HF_PRETRAINED_MODEL_NAME = "google/flan-t5-base" # "distilbert/distilbert-base-uncased"
HF_DATASET_NAME = "knkarthick/dialogsum"

TRAINING_EPOCHS = int(os.getenv("TRAINING_EPOCHS"))
TRAINING_BATCH_SIZE = int(os.getenv("TRAINING_BATCH_SIZE"))
TRAINING_LEARNING_RATE = float(os.getenv("TRAINING_LEARNING_RATE"))
TRAINING_DEVICE = "gpu" # one of ["cpu", "gpu", "mps"]

LORA_TARGET_MODULES=[
    "q",
    "v"
]
LORA_R = int(os.getenv("LORA_R"))
LORA_ALPHA = int(os.getenv("LORA_ALPHA"))
LORA_DROPOUT = float(os.getenv("LORA_DROPOUT"))

OUTPUT_DIRECTORY = os.path.join("trained", HF_PRETRAINED_MODEL_NAME)
HUGGINGFACE_REPO_ID = os.getenv("HUGGINGFACE_REPO_ID")

if TRAINING_DEVICE == "gpu":
    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

# %% gather={"logged": 1721941154263}
print(f"HF pretrained model name: {HF_PRETRAINED_MODEL_NAME}")
print(f"HF dataset name: {HF_DATASET_NAME}")

print(f"epochs: {TRAINING_EPOCHS}")
print(f"batch_size: {TRAINING_BATCH_SIZE}")
print(f"learning rate (lr): {TRAINING_LEARNING_RATE}")

print(f"LORA r: {LORA_R}")
print(f"LORA alpha: {LORA_ALPHA}")
print(f"LORA droupout: {LORA_DROPOUT}")

print(f"Using {TRAINING_DEVICE} device")

# %% [markdown] nteract={"transient": {"deleting": false}}
# # Download Training Data

# %% gather={"logged": 1721941186999}
# download datasets: train, validation, test
from datasets import load_dataset

dataset = load_dataset(HF_DATASET_NAME)  # doctest: +IGNORE_RESULT

# %% gather={"logged": 1721941187076}
import json

print(f"dataset: {list(dataset)}")
topics = set()
for dataset_key in dataset:
    print(f"len({dataset_key}): {len(dataset[dataset_key])}")
    [topics.add(t) for t in dataset[dataset_key]["topic"]]
print(f"train dataset: {dataset["train"]}")
print(f"train dataset features: {dataset["train"].features}")
print(f"topics ({len(topics)} unique), first 10: {[topics.pop() for i in range(10)]}")
for i in range(3):
    print(f"Example ({i}): {json.dumps(dataset["train"][i], indent=2)}")

# %% [markdown]
# # Model and Tokenizer

# %% gather={"logged": 1721941320624}
# download tokenizer
from transformers import T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained(HF_PRETRAINED_MODEL_NAME)

# %% gather={"logged": 1721941324149}
# download model
from transformers import T5ForConditionalGeneration

base_model = T5ForConditionalGeneration.from_pretrained(
    pretrained_model_name_or_path=HF_PRETRAINED_MODEL_NAME
)
base_model

# %% gather={"logged": 1721941329974}
# test inference
input_text = dataset["train"][0]["dialogue"]
print(f"==INPUT TEXT==:\n{input_text}")
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = base_model.generate(inputs=input_ids, max_length=4000)
print(f"==OUTPUT==:\n{tokenizer.decode(outputs[0])}")
print(f"==EXPECTED==:\n{dataset["train"][0]["summary"]}")


# %% [markdown]
# # Fine-tuning configuration

# %% gather={"logged": 1721941374429}
# tokenize the dataset
# Hugging Face Transformers models expect tokenized input, 
# rather than the text in the downloaded data.
def tokenize_dataset(dataset):
    prompt = [f"Summarize the following dialogue:\n\n{dialogue}\n\nSummary:"
              for dialogue in dataset["dialogue"]]
    dataset["input_ids"] = tokenizer(
        prompt,
        padding="max_length",
        truncation=True,
        return_tensors="pt").input_ids
    dataset["labels"] = tokenizer(
        dataset["summary"],
        padding="max_length",
        truncation=True,
        return_tensors="pt").input_ids
    return dataset

encoded_dataset = dataset.map(
    tokenize_dataset,
    batched=True,
    remove_columns=["id", "topic", "dialogue", "summary"])

# %% gather={"logged": 1721941377208}
import json

print(f"encoded dataset: {list(encoded_dataset)}")
for dataset_key in encoded_dataset:
    print(f"len({dataset_key}): {len(encoded_dataset[dataset_key])}")
print(f"train dataset: {encoded_dataset["train"]}")
print(f"train dataset features: {encoded_dataset["train"].features}")
for i in range(3):
    print(f"Example ({i}): {json.dumps(encoded_dataset["train"][i], indent=2)}")

# %% gather={"logged": 1721941379641}
# configure LoRA
from peft import LoraConfig, TaskType

peft_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,  # defines the expected fields of the tokenized dataset
    target_modules=LORA_TARGET_MODULES,  # model modules to apply LoRA to
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
)

# %% gather={"logged": 1721941381663}
# wrap model with PEFT config
from peft import get_peft_model

peft_wrapped_model = get_peft_model(base_model, peft_config)
peft_wrapped_model.print_trainable_parameters()

# %% [markdown]
# # Training Job

# %% [markdown]
# ## Training with Transformers for Pytorch

# %% gather={"logged": 1721941386203}
# data loader/collator to batch input in training and evaluation datasets
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# %% gather={"logged": 1721941388782} jupyter={"outputs_hidden": false, "source_hidden": false} nteract={"transient": {"deleting": false}}
# configure evaluation metrics
# in addition to the default `loss` metric that the `Trainer` computes
import evaluate
import numpy as np

evaluation_module = evaluate.load("accuracy")

def compute_metrics(eval_pred, evaluation_module=evaluation_module):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return evaluation_module.compute(predictions=predictions, references=labels)


# %% gather={"logged": 1721941393185} jupyter={"outputs_hidden": false, "source_hidden": false} nteract={"transient": {"deleting": false}}
# [OPTIONAL] clean up the GPU memory
if TRAINING_DEVICE == "gpu":
    from numba import cuda
    device = cuda.get_current_device()
    device.reset()

# %% gather={"logged": 1721941393339}
# train job config
# Hugging Face training configuration tools can be used to configure a Trainer.
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir=OUTPUT_DIRECTORY,

    #do_train=True,
    #do_eval=True,

    num_train_epochs=TRAINING_EPOCHS,
    per_device_train_batch_size=TRAINING_BATCH_SIZE,
    per_device_eval_batch_size=TRAINING_BATCH_SIZE,
    learning_rate=TRAINING_LEARNING_RATE,

    weight_decay=0.01,
    #gradient_accumulation_steps=2,  # default 1
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    # metric_for_best_model="f1"

    #fp16=True,  # lower precision
    # use_ipex=True if DEVICE == "cpu" else False,  # use Intel extension for PyTorch
    use_cpu=TRAINING_DEVICE == "cpu"  # False will use CUDA or MPS if available
)

# %% gather={"logged": 1721941396223}
# The Trainer classes require the user to provide: 1) Metrics 2) A base model 3) A training configuration
from transformers import Trainer

trainer = Trainer(
    model=peft_wrapped_model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    # compute_metrics=compute_metrics
)

# %% gather={"logged": 1721941403821}
trainer.train()

# %% [markdown]
# # Store Model

# %% gather={"logged": 1721939469374}
# save model
import os

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
peft_wrapped_model.save_pretrained(OUTPUT_DIRECTORY)
tokenizer.save_pretrained(OUTPUT_DIRECTORY)

# %% gather={"logged": 1721939469382}
# save on Huggingface
from huggingface_hub import notebook_login

notebook_login()
peft_wrapped_model.push_to_hub(HUGGINGFACE_REPO_ID)
