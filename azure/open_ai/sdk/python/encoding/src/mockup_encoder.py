import string
import logging
from typing import List

from src.encoder import Encoder


class MockupEmbeddingGenerator(Encoder):
    """
    Class for generate embeddings
    """
    model: str = 'mockup'

    def __init__(self):
        logging.info("Start MockUp base configuration ...")

        logging.info("Completed MockUp base configuration.")

    def encode(self, text: str) -> List[float]:
        """
        Generate embeddings
        @param text: text to generate embeddings
        @return: embeddings
        """

        embeddings = dict()
        for char in string.printable + string.whitespace:
            embeddings[char] = 0

        for char in text:
            embeddings[char] = embeddings.get(char, 0) + 1

        return list(embeddings.values())
