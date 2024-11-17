# HF:facebook/roberta-hate-speech-dynabench-r4-target
# https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target

from transformers import pipeline

pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")

# The following examples of harmful content that may be disturbing to some readers
test_data = [(
    "Trumps' tweet: "
    "go back and help fix the totally broken " 
    "and crime infested places from which they came"
    ), (
    "Azure's example text on hate: "
    "[Identity Group] threaten our existence, so we should wipe them out."
    # https://learn.microsoft.com/en-gb/azure/ai-services/openai/concepts/content-filter?tabs=definitions%2Cuser-prompt%2Cpython-new#risk-categories
)]

pipe(test_data)
