# BERTScore

import evaluate

bertscore = evaluate.load("bertscore")

predictions = ["hello there", "general kenobi"]
references = ["hello there", "general kenobi"]

print(bertscore.compute(predictions=predictions, references=references, lang="en"))