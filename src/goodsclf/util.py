import re
from typing import List

from nltk.tokenize import wordpunct_tokenize


def _split_by_case(word):
    return re.split(r"[A-ZА-Я][a-zа-я0-9]+", word)


def _split_by_numbers(word):
    return re.split(r"(\d+)", word)


def clean_data(text: List[str]) -> List[str]:
    text = " ".join(_split_by_numbers(text))
    return " ".join(
        [word.lower() for word in wordpunct_tokenize(text) if word.isalnum()]
    )
