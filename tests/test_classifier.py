from goodsclf.classifier import GoodsClassifier


def test_classifier_load():
    clf = GoodsClassifier()
    clf.load()
