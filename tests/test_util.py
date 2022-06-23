from goodsclf.util import clean_data


def test_clean_data():
    data = [
        ("Golden Apples, 500g LIDL", "golden apples lidl"),
        ("AA,BB.CC-DD!", "aa bb cc-dd"),
    ]

    for item in data:
        a, e = item
        assert e == clean_data(a)
