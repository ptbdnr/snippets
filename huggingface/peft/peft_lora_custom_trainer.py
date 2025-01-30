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
# # Parameter-Efficient Finetuning (PEFT) with Low-Level Adaptation (LORA) using HuggingFace PEFT on a single GPU

# %%
# %pip install -q -r ./../requirements.txt
# %pip install -q --force-reinstall numpy==1.26.4

# %%
import numpy as np
import torch

print(torch.__version__)
print(np.__version__)

# "2.5.1"
# "1.26.4"

# %%
# input constants
import os

import dotenv

dotenv.load_dotenv()

HF_PRETRAINED_MODEL_NAME = "distilbert-base-uncased"
HF_DATASET_COLLECTION = "glue"
HF_DATASET_CONFIG_NAME = "mrpc"  # Microsoft Research Paraphrase Corpus

TRAINING_EPOCHS = int(os.getenv("TRAINING_EPOCHS"))
TRAINING_BATCH_SIZE = int(os.getenv("TRAINING_BATCH_SIZE"))
TRAINING_LEARNING_RATE = float(os.getenv("TRAINING_LEARNING_RATE"))
TRAINING_DEVICE = "gpu" # one of ["cpu", "gpu", "mps"]

LORA_TARGET_MODULES = [
    "attention.q_lin", 
    "attention.k_lin", 
    "attention.v_lin", 
    "attention.out_lin"
]
LORA_R = int(os.getenv("LORA_R"))
LORA_ALPHA = int(os.getenv("LORA_ALPHA"))
LORA_DROPOUT = float(os.getenv("LORA_DROPOUT"))

OUTPUT_DIRECTORY = os.path.join("trained", HF_PRETRAINED_MODEL_NAME)
HUGGINGFACE_REPO_ID = os.getenv("HUGGINGFACE_REPO_ID")

# %%
print(f"HF pretrained model name: {HF_PRETRAINED_MODEL_NAME}")
print(f"HF datasets name: {HF_DATASET_COLLECTION}")
print(f"HF task name: {HF_DATASET_CONFIG_NAME}")

print(f"epochs: {TRAINING_EPOCHS}")
print(f"batch_size: {TRAINING_BATCH_SIZE}")
print(f"learning rate (lr): {TRAINING_LEARNING_RATE}")

print(f"LORA r: {LORA_R}")
print(f"LORA alpha: {LORA_ALPHA}")
print(f"LORA droupout: {LORA_DROPOUT}")

print(f"Using {TRAINING_DEVICE} device")

# %% [markdown]
# # Download Training Data

# %%
# download datasets: train, validation, test
from datasets import load_dataset

dataset = load_dataset(HF_DATASET_COLLECTION, HF_DATASET_CONFIG_NAME, trust_remote_code=True)  # doctest: +IGNORE_RESULT

# /anaconda/envs/azureml_py310_sdkv2/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
#   from .autonotebook import tqdm as notebook_tqdm
# Downloading readme: 100%|██████████| 35.3k/35.3k [00:00<00:00, 51.0MB/s]
# Downloading data: 100%|██████████| 649k/649k [00:00<00:00, 1.47MB/s]
# Downloading data: 100%|██████████| 75.7k/75.7k [00:00<00:00, 249kB/s]
# Downloading data: 100%|██████████| 308k/308k [00:00<00:00, 1.02MB/s]
# Generating train split: 100%|██████████| 3668/3668 [00:00<00:00, 16329.64 examples/s]
# Generating validation split: 100%|██████████| 408/408 [00:00<00:00, 216370.72 examples/s]
# Generating test split: 100%|██████████| 1725/1725 [00:00<00:00, 560605.49 examples/s]

# %%
print(f"dataset: {list(dataset)}")

# %% [markdown]
# # Model and Tokenizer

# %%
# download tokenizer
from transformers import DistilBertTokenizer

tokenizer = DistilBertTokenizer.from_pretrained(HF_PRETRAINED_MODEL_NAME)

# %%
# download model
import torch
from transformers import DistilBertForSequenceClassification

base_model = DistilBertForSequenceClassification.from_pretrained(HF_PRETRAINED_MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
base_model.to(device)

# Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ["classifier.bias", "classifier.weight", "pre_classifier.bias", "pre_classifier.weight"]
# You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
# DistilBertForSequenceClassification(
#   (distilbert): DistilBertModel(
#     (embeddings): Embeddings(
#       (word_embeddings): Embedding(30522, 768, padding_idx=0)
#       (position_embeddings): Embedding(512, 768)
#       (LayerNorm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
#       (dropout): Dropout(p=0.1, inplace=False)
#     )
#     (transformer): Transformer(
#       (layer): ModuleList(
#         (0-5): 6 x TransformerBlock(
#           (attention): MultiHeadSelfAttention(
#             (dropout): Dropout(p=0.1, inplace=False)
#             (q_lin): Linear(in_features=768, out_features=768, bias=True)
#             (k_lin): Linear(in_features=768, out_features=768, bias=True)
#             (v_lin): Linear(in_features=768, out_features=768, bias=True)
#             (out_lin): Linear(in_features=768, out_features=768, bias=True)
#           )
#           (sa_layer_norm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
#           (ffn): FFN(
#             (dropout): Dropout(p=0.1, inplace=False)
#             (lin1): Linear(in_features=768, out_features=3072, bias=True)
#             (lin2): Linear(in_features=3072, out_features=768, bias=True)
#             (activation): GELUActivation()
#           )
#           (output_layer_norm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
#         )
#       )
#     )
#   )
#   (pre_classifier): Linear(in_features=768, out_features=768, bias=True)
#   (classifier): Linear(in_features=768, out_features=2, bias=True)
#   (dropout): Dropout(p=0.2, inplace=False)
# )

# %% [markdown]
# # Fine-tuning configuration

# %%
# tokenize the dataset
# Hugging Face Transformers models expect tokenized input, 
# rather than the text in the downloaded data.
def tokenize_dataset(examples):
    return tokenizer(examples["sentence1"], examples["sentence2"], truncation=True, padding="max_length")

train_dataset = dataset["train"]
test_dataset = dataset["test"]
validation_dataset = dataset["validation"]

encoded_training_dataset = train_dataset.map(tokenize_dataset, batched=True)
encoded_validation_dataset = validation_dataset.map(tokenize_dataset, batched=True)
encoded_test_dataset = test_dataset.map(tokenize_dataset, batched=True)

encoded_training_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
encoded_validation_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
encoded_test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# Map: 100%|██████████| 3668/3668 [00:03<00:00, 966.31 examples/s]
# Map: 100%|██████████| 408/408 [00:00<00:00, 1003.11 examples/s]
# Map: 100%|██████████| 1725/1725 [00:01<00:00, 1021.17 examples/s]

# %%
print(f"len(training): {len(encoded_training_dataset)}")
print(f"len(validation): {len(encoded_validation_dataset)}")
print(f"len(test): {len(encoded_test_dataset)}")

# %%
# configure LoRA
from peft import LoraConfig

lora_config = LoraConfig(
    target_modules=LORA_TARGET_MODULES,
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    bias="none"  # exclude bias
)

# %%
# wrap model with PEFT config
from peft import get_peft_model

peft_wrapped_model = get_peft_model(base_model, lora_config)
peft_wrapped_model.print_trainable_parameters()

# trainable params: 294,912 || all params: 67,249,922 || trainable%: 0.4385

# %% [markdown]
# # Training Job

# %%
# configure evaluation metrics
# in addition to the default `loss` metric that the `Trainer` computes
import evaluate
import torch
from torch.nn.functional import softmax

evaluation_module = evaluate.load(HF_DATASET_COLLECTION, HF_DATASET_CONFIG_NAME)

def evaluate_model(model, data_loader, device, evaluation_module=evaluation_module):
    """ Evaluate the model on the given data loader """
    model.eval()
    all_predictions = []
    all_labels = []
    all_probabilities = []
    total_eval_loss = 0
    with torch.no_grad():
        for batch in data_loader:
            inputs = {key: val.to(device) for key, val in batch.items() if key != "label"}
            labels = batch["label"].to(device)

            outputs = model(**inputs, labels=labels)
            logits = outputs.logits
            loss = outputs.loss
            total_eval_loss += loss.item()

            probs = softmax(logits, dim=-1)

            positive_probs = probs[:, 1]
            all_probabilities.extend(positive_probs.cpu().numpy())

            predictions = torch.argmax(logits, dim=-1)

            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    avg_loss = total_eval_loss / len(data_loader)

    results = evaluation_module.compute(predictions=all_predictions, references=all_labels)
    results["eval_loss"] = avg_loss
    results["probs"] = all_probabilities
    results["labels"] = all_labels
    return results

# Downloading builder script: 100%|██████████| 5.75k/5.75k [00:00<00:00, 19.5MB/s]


# %%
# [OPTIONAL] clean up the GPU memory
if TRAINING_DEVICE == "gpu":
    from numba import cuda
    device = cuda.get_current_device()
    device.reset()

# %%
# train job config
from transformers import AdamW


def train_model(
        model,
        train_loader,
        validation_loader,
        device,
        num_epochs=TRAINING_EPOCHS,
        learning_rate=TRAINING_LEARNING_RATE
):
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    training_stats = []
    for epoch in range(num_epochs):
        total_train_loss = 0
        model.train()
        for batch in train_loader:
            optimizer.zero_grad()
            inputs = {key: val.to(device) for key, val in batch.items() if key != "label"}
            labels = batch["label"].to(device)

            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)
        validation_results = evaluate_model(model, validation_loader, device)
        training_stats.append({
            "epoch": epoch + 1,
            "Training Loss": avg_train_loss,
            "Validation Loss": validation_results["eval_loss"],
            "Validation Accuracy": validation_results["accuracy"]
        })

        print(f"Epoch {epoch + 1} | "
            f"Training Loss: {avg_train_loss:.4f} | "
            f"Validation Loss: {validation_results["eval_loss"]:.4f} | "
            f"Validation Accuracy: {validation_results["accuracy"]:.4f}"
        )



# %%
# data loader/collator to batch input in training and evaluation datasets
from torch.utils.data import DataLoader

train_loader = DataLoader(
    encoded_training_dataset,
    batch_size=TRAINING_BATCH_SIZE,
    shuffle=True
)

validation_loader = DataLoader(
    encoded_validation_dataset,
    batch_size=TRAINING_BATCH_SIZE,
    shuffle=False
)

test_loader = DataLoader(
    encoded_test_dataset,
    batch_size=TRAINING_BATCH_SIZE,
    shuffle=False
)

# %%
# train
train_model(peft_wrapped_model, train_loader, validation_loader, device)

# /anaconda/envs/azureml_py310_sdkv2/lib/python3.10/site-packages/transformers/optimization.py:591: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
#   warnings.warn(
# Epoch 1 | Training Loss: 0.6517 | Validation Loss: 0.6054 | Validation Accuracy: 0.6838
# Epoch 2 | Training Loss: 0.5940 | Validation Loss: 0.5654 | Validation Accuracy: 0.6838
# Epoch 3 | Training Loss: 0.5571 | Validation Loss: 0.5354 | Validation Accuracy: 0.7010
# Epoch 4 | Training Loss: 0.5148 | Validation Loss: 0.4781 | Validation Accuracy: 0.7328
# Epoch 5 | Training Loss: 0.4663 | Validation Loss: 0.5124 | Validation Accuracy: 0.7892
# Epoch 6 | Training Loss: 0.4258 | Validation Loss: 0.4324 | Validation Accuracy: 0.8186
# Epoch 7 | Training Loss: 0.3962 | Validation Loss: 0.3761 | Validation Accuracy: 0.8211
# Epoch 8 | Training Loss: 0.3706 | Validation Loss: 0.3743 | Validation Accuracy: 0.8333
# Epoch 9 | Training Loss: 0.3612 | Validation Loss: 0.3577 | Validation Accuracy: 0.8333
# Epoch 10 | Training Loss: 0.3445 | Validation Loss: 0.3618 | Validation Accuracy: 0.8407
# Epoch 11 | Training Loss: 0.3223 | Validation Loss: 0.3639 | Validation Accuracy: 0.8382
# Epoch 12 | Training Loss: 0.3097 | Validation Loss: 0.3468 | Validation Accuracy: 0.8431
# Epoch 13 | Training Loss: 0.3045 | Validation Loss: 0.3538 | Validation Accuracy: 0.8407
# Epoch 14 | Training Loss: 0.2839 | Validation Loss: 0.3681 | Validation Accuracy: 0.8358
# Epoch 15 | Training Loss: 0.2716 | Validation Loss: 0.3757 | Validation Accuracy: 0.8480
# Epoch 16 | Training Loss: 0.2630 | Validation Loss: 0.3404 | Validation Accuracy: 0.8554
# Epoch 17 | Training Loss: 0.2538 | Validation Loss: 0.3730 | Validation Accuracy: 0.8407
# Epoch 18 | Training Loss: 0.2367 | Validation Loss: 0.3658 | Validation Accuracy: 0.8529
# Epoch 19 | Training Loss: 0.2245 | Validation Loss: 0.3713 | Validation Accuracy: 0.8578
# Epoch 20 | Training Loss: 0.2191 | Validation Loss: 0.3800 | Validation Accuracy: 0.8480
# Epoch 21 | Training Loss: 0.2095 | Validation Loss: 0.4098 | Validation Accuracy: 0.8480
# Epoch 22 | Training Loss: 0.1957 | Validation Loss: 0.4107 | Validation Accuracy: 0.8529
# Epoch 23 | Training Loss: 0.1860 | Validation Loss: 0.4176 | Validation Accuracy: 0.8554

# %% [markdown]
# # Evaluate Model

# %%
# evaluate the base model
base_results = evaluate_model(base_model, test_loader, device)
filtered_base_results = {
    key: value for key, value in base_results.items()
    if key not in ["probs", "labels"]
}
print("Base Model eval:", filtered_base_results)

# Base Model eval: {"accuracy": 0.36869565217391304, "f1": 0.21710999281092738, "eval_loss": 0.701879393171381}

# %%
# eval peft model
peft_results = evaluate_model(peft_wrapped_model, test_loader, device)
filtered_peft_results = {
    key: value for key, value in peft_results.items()
    if key not in ["probs", "labels"]
}
print("Fine-Tuned Model eval:", filtered_peft_results)

# Fine-Tuned Model eval: {"accuracy": 0.8266666666666667, "f1": 0.873036093418259, "eval_loss": 0.47620911665122817}

# %%
print("Base Model eval:", filtered_base_results)
print("Fine-Tuned Model eval:", filtered_peft_results)

# Base Model eval: {"accuracy": 0.36869565217391304, "f1": 0.21710999281092738, "eval_loss": 0.701879393171381}
# Fine-Tuned Model eval: {"accuracy": 0.8266666666666667, "f1": 0.873036093418259, "eval_loss": 0.47620911665122817}

# %% [markdown]
# # Store Model

# %%
# save model
import os

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
peft_wrapped_model.save_pretrained(OUTPUT_DIRECTORY)
tokenizer.save_pretrained(OUTPUT_DIRECTORY)

# ("./../data/ft_model/tokenizer_config.json",
#  "./../data/ft_model/special_tokens_map.json",
#  "./../data/ft_model/vocab.txt",
#  "./../data/ft_model/added_tokens.json")

# %%
# save on Huggingface
from huggingface_hub import notebook_login

notebook_login()
peft_wrapped_model.push_to_hub(HUGGINGFACE_REPO_ID)
