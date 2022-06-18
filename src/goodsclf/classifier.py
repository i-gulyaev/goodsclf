import pickle
from importlib.resources import files
from typing import Dict, List

import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.utils.multiclass import unique_labels

from .util import clean_data


class GoodsClassifier:
    def __init__(self):
        self.transformer = None
        self.model = None
        self.labels = None

    def load_default(self):
        transformer = files("goodsclf.data").joinpath("transformer.pickle")
        model = files("goodsclf.data").joinpath("model.pickle")
        labels = files("goodsclf.data").joinpath("labels.pickle")

        with transformer.open(mode="rb") as t, model.open(
            mode="rb"
        ) as m, labels.open(mode="rb") as lb:
            self.transformer = pickle.load(t)
            self.model = pickle.load(m)
            self.labels = pickle.load(lb)

            return self

    def load(
        self,
        transformer: str = "",
        model: str = "",
        labels: str = "",
    ):
        if not transformer and not model and not labels:
            return self.load_default()
        else:
            with open(transformer, "rb") as t, open(model, "rb") as m, open(
                labels, "rb"
            ) as lb:
                self.transformer = pickle.load(t)
                self.model = pickle.load(m)
                self.labels = pickle.load(lb)

                return self

    def predict(self, data: List[str]) -> List[str]:
        assert self.transformer
        assert self.model
        assert self.labels

        cleaned_data = [clean_data(item) for item in data]
        test = self.transformer.transform(cleaned_data).toarray()
        pred = self.model.predict(test)

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

        df = pd.DataFrame(train_data)
        df["item"] = df["item"].apply(clean_data)
        df["label_id"] = df["label"].factorize()[0]

        self.transformer = TfidfTransformer(
            sublinear_tf=True,
            min_df=5,
            norm="l2",
            ngram_range=(1, 2),
        )
        features = self.transformer.fit_transform(df["item_name"]).toarray()
        labels = df["label_id"]

        self.labels = dict(
            df[["label", "id"]].drop_duplicates().sort_values("id").values()
        )

        (
            X_train,
            X_test,
            y_train,
            y_test,
            indices_train,
            indices_test,
        ) = train_test_split(
            features, labels, df.index, test_size=0.33, random_state=42
        )

        self.model = LinearSVC()
        self.model.fit(X_train, y_train)

        if show_clf_report:
            y_pred = self.model.predict(X_test)
            target_names = [
                self.labels[id] for id in unique_labels(y_test, y_pred)
            ]
            print(
                metrics.classification_report(
                    y_test,
                    y_pred,
                    target_names=target_names,
                )
            )

    def save(
        self,
        transformer: str,
        model: str,
        labels: str,
    ):
        pickle.dump(self.transformer, open(transformer, "wb"))
        pickle.dump(self.model, open(model, "wb"))
        pickle.dump(self.labels, open(labels, "wb"))
