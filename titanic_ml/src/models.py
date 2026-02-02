from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from data_processing import build_preprocessor


def decision_tree_model():
    return Pipeline([
        ("preprocessing", build_preprocessor()),
        ("classifier", DecisionTreeClassifier(
            random_state=42,
            max_depth=None
        ))
    ])

def logistic_regression_model():
    return Pipeline([
        ("preprocessing", build_preprocessor()),
        ("classifier", LogisticRegression(
            max_iter=1000,
            random_state=42
        ))
    ])