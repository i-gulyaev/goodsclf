import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ["nltk", "pandas", "scikit-learn"]

PKG_NAME = "goodsclf"

setuptools.setup(
    name=PKG_NAME,
    version="0.0.1",
    author="IG",
    author_email="author@example.com",
    description="Goods classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
        f"{PKG_NAME}.data": [
            "estimator.pickle",
            "labels.pickle",
        ],
    },
    python_requires=">=3.6",
    install_requires=install_requires,
)
