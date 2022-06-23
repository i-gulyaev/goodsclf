import re


def clean_data(text: str) -> str:
    # "AaAa" -> "aaaa"
    text = text.lower()

    # "100 г" -> "100г"
    text = re.sub(r"(\d+)\s+(г|кг|л|мл|шт)", r"\1\2", text)

    # "milk100ml" -> "milk 100ml"
    text = re.sub(r"([a-zа-я]{2,})(\d+)", r"\1 \2", text)

    # remove punctuation
    text = re.sub(r"[\.,:?!\'\"\*]", " ", text)

    # "111-111" -> "111 111"
    text = re.sub(r"(\d+)-(\d+)", r"\1 \2", text)

    # "100%100" -> "100"
    # "100ml " -> ""
    text = re.sub(
        r"\d+\s?(шт|г|кг|л|мл|м|см|ш|шт|l|ml|g|kg|%|-)(\s|\d+|$)", "", text
    )

    # remove counts
    text = re.sub(r" (шт|г|кг|л|мл|l|ml|%)$", "", text)

    # "№ 2" -> "2"
    text = re.sub(r"№\s+?(\d+)", r"\1", text)

    # "2x" -> ""
    # "2x2x2" -> "2"
    text = re.sub(r"\d+[xх]", "", text)

    return " ".join([word for word in text.split() if not word.isdigit()])
