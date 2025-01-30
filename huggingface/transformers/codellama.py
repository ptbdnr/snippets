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

# %%
# %pip install -r requirements.txt

# %%
# input constants
import dotenv
import torch

dotenv.load_dotenv()

HF_PRETRAINED_MODEL_NAME = "codellama/CodeLlama-7b-Python-hf"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # when debugging use "cpu" for better error messages


# %%
print(f"HF pretrained model name: {HF_PRETRAINED_MODEL_NAME}")

print(f"Using {DEVICE} device")

# %%
# using pipelines
from transformers import pipeline

text_generation = pipeline("text-generation", model=HF_PRETRAINED_MODEL_NAME, device=DEVICE)

# %%
text_generation("write a function to generate fibonacci sequence", truncation=False)
