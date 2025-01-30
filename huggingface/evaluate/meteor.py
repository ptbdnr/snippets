# METEOR

import json

import evaluate

meteor = evaluate.load("meteor")
predictions = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
references = ["It is a guide to action that ensures that the military will forever heed Party commands"]

score = meteor.compute(predictions=predictions, references=references) 
print(json.dumps(score, indent=2))
