# ###################
# MoverScore
# KNOWN ISSUE: dependency versions are incorrect

# Python 3.10
# moverscore==1.0.3
# "numpy<2.0.0,>=1.9.0"
# torch-2.5.1
# pyemd==0.5.1
# pytorch-transformers==1.1.0


# Use the original version with BERTMNLI to reproduce the results.
#from moverscore import get_idf_dict, word_mover_score
# Recommend to use this version (DistilBERT) for evaluation, if the speed is your concern.
from moverscore_v2 import get_idf_dict, word_mover_score 
from collections import defaultdict

predictions = ["hello there", "London, UK", "yoga"]
references = ["hello there", "capital of Great Britan", ""]

idf_dict_hyp = get_idf_dict(predictions) # idf_dict_hyp = defaultdict(lambda: 1.)
idf_dict_ref = get_idf_dict(references) # idf_dict_ref = defaultdict(lambda: 1.)

scores = word_mover_score(references, predictions, idf_dict_ref, idf_dict_hyp, \
                          stop_words=[], n_gram=1, remove_subwords=True)
print(scores)