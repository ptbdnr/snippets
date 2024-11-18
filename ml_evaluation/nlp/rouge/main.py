import json

from rouge_score import rouge_scorer

# ROUGE n-gram is rougeN (eg. rouge1, rouge2)
# ROUTE Longest common subsequence based scoring is rougeL
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
scores = scorer.score(
    target='The quick brown fox jumps over the lazy dog',
    prediction='The quick brown dog jumps on the log.'
)
# output format precision, recall, fmeasure
print(json.dumps(scores, indent=2))