import pickle
from importlib.resources import files
from typing import Dict, List

from .util import clean_data


class GoodsClassifier:
    def __init__(self):
        self.estimator_ = None
        self.labels = None

    def load_default(self):
        estimator = files("goodsclf.data").joinpath("estimator.pickle")
        labels = files("goodsclf.data").joinpath("labels.pickle")

        with estimator.open(mode="rb") as e, labels.open(mode="rb") as lb:
            self.estimator = pickle.load(e)
            self.labels = pickle.load(lb)

            return self

    def load(
        self,
        estimator: str = "",
        labels: str = "",
    ):
        if not estimator and not labels:
            return self.load_default()
        else:
            with open(estimator, "rb") as e, open(labels, "rb") as lb:
                self.estmator = pickle.load(e)
                self.labels = pickle.load(lb)

                return self

    def predict(self, data: List[str]) -> List[str]:
        assert self.estimator
        assert self.labels is not None

        cleaned_data = [clean_data(item) for item in data]
        pred = self.estimator.predict(cleaned_data)

        return [self.labels[idx] for idx in pred]

    def update(
        self,
        train_data: Dict[str, List[str]],
        labels: List[str],
        show_clf_report=False,
    ):
        """
        Update data transformer and classification model using
        given 'train_data' and 'labels'.

        - 'train_data': dictionary of form '{"item: [], "label": []}'
                        that contains new dataset
        - 'labels': list of labels used by classifier.
        """
        pass

    def save(
        self,
        transformer: str,
        model: str,
        labels: str,
    ):
        pass
