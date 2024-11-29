"""
Spacy is a library for advanced Natural Language Processing
in Python and Cython. It's designed specifically for
production use and helps build applications that process
and “understand” large volumes of text. It can be used to
build information extraction or natural language understanding systems,
or to pre-process text for deep learning.

Features
Tokenization: Segmenting text into words, punctuations marks etc.
Lemmatization: Assigning the base forms of words. For example,
the lemma of “was” is “be”, and the lemma of “rats” is “rat”.
Part-of-speech (POS) Tagging: Assigning word types to tokens,
like verb or noun.

Dependency Parsing: Assigning syntactic dependency labels,
describing the relations between individual tokens, like subject or object.
Sentence Boundary Detection (SBD): Finding and segmenting individual sentences.
Named Entity Recognition (NER): Labelling named “real-world” objects,
like persons, companies or locations.
Entity Linking (EL): Disambiguating textual entities
to unique identifiers in a knowledge base.
Similarity: Comparing words, text spans and documents
and how similar they are to each other.
Text Classification: Assigning categories or labels to a whole document,
or parts of a document.
Rule-based Matching: Finding sequences of tokens based on their texts
and linguistic annotations, similar to regular expressions.
Training: Updating and improving a statistical model’s predictions.
Serialization: Saving objects to files or byte strings.
"""

# Prerequisites
# Option 1:
# python3 -m spacy download en_core_web_sm
# Option 2:
# python3 -m spacy download en_core_web_sm-2.2.5 --direct
# Option 3:
# wget https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz
# python -m pip install ./en_core_web_sm-2.2.5.tar.gz
# Option 4: only one of
# pip --trusted-host github.com --trusted-host objects.githubusercontent.com install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz
# pip --trusted-host github.com --trusted-host objects.githubusercontent.com install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz

import spacy

nlp = spacy.load(name="en_core_web_sm")

doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# tokenise the text i.e. segment it into words, punctuation and so on
for token in doc:
    item = {
        "text": token.text,  # original word text
        "lemma": token.lemma_,  # base form of the word
        "POS": token.pos_,  # Universal Part-Of-Speech (UPOS) tag
        "tag": token.tag_,  # detailed POS
        "dep": token.dep_,  # syntactic dependency
        "shape": token.shape_,  # capitalisation (X or x), digits (d), etc
        "is_alpha": token.is_alpha,  # consists of alphabetic chars
        "is_stop": token.is_stop,  # is part of a stop list (most common words)
    }
    print(item)
    print({k: spacy.explain(v) for (k, v) in item.items()
           if k in ["POS", "tag", "dep"]})

# Named Entity Recognition
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

for ent in doc.ents:
    item = {
        "text": ent.text,  # original word text
        "start_char": ent.start_char,  # start index of the entity
        "end_char": ent.end_char,  # end index of the entity
        "label": ent.label_,  # entity label, i.e. type.
    }
    print(item, spacy.explain(item['label']))

# Visualise the dependency parse
spacy.displacy.serve(doc, style="dep", options={"compact": True})
spacy.displacy.serve(doc, style="ent")
