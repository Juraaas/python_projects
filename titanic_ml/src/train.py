import pandas as pd
from sklearn.model_selection import train_test_split
from src.models import decision_tree_model
from src.data_processing import FEATURE_COLUMNS, TARGET_COLUMN

def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load raw dataset from CSV.
    """
    return pd.read_csv(csv_path)


def split_features_target(df: pd.DataFrame):
    """
    Split dataset into features (X) and target (y).
    """
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y


def train(model_fn, csv_path: str):
    """
    Train model using full training dataset.
    """
    df = pd.read_csv(csv_path)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    model = model_fn()
    model.fit(X, y)

    return model
