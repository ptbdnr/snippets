import textstat

test_data = (
    "Playing games has always been thought to be important to "
    "the development of well-balanced and creative children; "
    "however, what part, if any, they should play in the lives "
    "of adults has never been researched that deeply. I believe "
    "that playing games is every bit as important for adults "
    "as for children. Not only is taking time out to play games "
    "with our children and other adults valuable to building "
    "interpersonal relationships but is also a wonderful way "
    "to release built up tension."
)

print(f"Letter count: {textstat.letter_count(test_data)}")
print(f"Word count: {textstat.lexicon_count(test_data)}")
print(f"Sentence count: {textstat.sentence_count(test_data)}")
print(f"FK grade: {textstat.flesch_kincaid_grade(test_data)}")
print(f"ARI: {textstat.automated_readability_index(test_data)}")

