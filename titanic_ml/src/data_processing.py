from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

NUM_FEATURES = [
    "Age",
    "Fare",
    "SibSp",
    "Parch"
]

CAT_FEATURES = [
    "Sex",
    "Pclass"
]

FEATURE_COLUMNS = NUM_FEATURES + CAT_FEATURES
TARGET_COLUMN = "Survived"

def build_numeric_pipeline():
    return Pipeline([
        ("imputer", SimpleImputer(strategy="mean"))
    ])

def build_categorical_pipeline():
    return Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
    ])

def build_preprocessor():
    numeric_pipeline = build_numeric_pipeline()
    categorical_pipeline = build_categorical_pipeline()

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, NUM_FEATURES),
        ("cat", categorical_pipeline, CAT_FEATURES)
    ])

    return preprocessor