import json

from wefe.query import Query
from wefe.word_embedding_model import WordEmbeddingModel
from wefe.metrics.WEAT import WEAT
import gensim.downloader as api

# Bias with WEFE: designed for embedding models

# load glove
twitter_25 = api.load('glove-twitter-25')
model = WordEmbeddingModel(twitter_25, 'glove twitter dim=25')

target_sets = {
    'Female Terms': ['she', 'woman', 'girl'],
    'Male Terms': ['he', 'man', 'boy']
}
attribute_sets = {
    'Arts': ['poetry','dance','literature'],
    'Science': ['math', 'physics', 'chemistry']
}

# create the query
query = Query(
    list(target_sets.values()), 
    list(attribute_sets.values()), 
    list(target_sets.keys()),
    list(attribute_sets.keys()))

print(json.dumps(WEAT().run_query(query, model), indent=2))
