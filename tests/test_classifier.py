from goodsclf.classifier import GoodsClassifier


def test_classifier_load_default():
    clf = GoodsClassifier()
    clf.load()


def test_classifier_predict():
    clf = GoodsClassifier()
    data = [
        "Сыр \"Страчателла\",шт",
        "Вода пит СВЯТОЙ ИСТОЧНИК н/газ 5L ПЭТ",
        "П/ф Стейк из лосося атл.охл вес",
        "Авокадо Хасс ready to eat  2шт",
    ]
    expected = ["Молоко/Сыр", "Вода", "Мясо/Рыба", "Овощи/Фрукты"]
    result = clf.load().predict(data)
    assert expected == result
