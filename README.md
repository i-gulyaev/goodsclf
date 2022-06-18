# Goods Classifier

[![Build and test](https://github.com/i-gulyaev/goodsclf/actions/workflows/ci-tests.yml/badge.svg?branch=main)](https://github.com/i-gulyaev/goodsclf/actions/workflows/ci-tests.yml)


## Usage

```python
from goodsclf import GoodsClassifier

clf = GoodsClassifier()
data = ["Apples", "Oranges", "Milk"]
result = clf.load().predict(data)

for item, label in zip(data, result):
    print(f"item: '{item}'; label: '{label}'")
```
