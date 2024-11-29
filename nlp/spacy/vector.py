# python -m spacy download en_core_web_lg

import spacy

nlp = spacy.load("en_core_web_md")  # make sure to use larger package!

doc1 = nlp("I like salty fries and hamburgers.")
doc2 = nlp("Fast food tastes very good.")

for token in doc1:
    item = {
        "text": token.text,
        "has_vector": token.has_vector,
        "vector_norm": token.vector_norm,
        "is_oov": token.is_oov,
    }
    print(item)

for token in doc1:
    lexeme = doc1.vocab[token.text]
    item = {
        "text": lexeme.text,  # the original text
        "orth": lexeme.orth,  # the hash value
        "shape": lexeme.shape_,  # the abstract word shape
        "prefix": lexeme.prefix_,  # the first char
        "suffix": lexeme.suffix_,  # the last 3 chars
        "is_alpha": lexeme.is_alpha,  # consists of alphabetic chars
        "is_digit": lexeme.is_digit,  # consist of digits
        "is_title": lexeme.is_title,  # starts with an uppercase
        "lang": lexeme.lang_,  # language
    }
    print(item)

# Similarity of two documents
print(doc1, "<->", doc2, doc1.similarity(doc2))

# Similarity of tokens and spans
french_fries = doc1[2:4]
burgers = doc1[5]
print(french_fries, "<->", burgers, french_fries.similarity(burgers))
